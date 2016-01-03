! Sam(oa)² - SFCs and Adaptive Meshes for Oceanic And Other Applications
! Copyright (C) 2010 Oliver Meister, Kaveh Rahnema
! This program is licensed under the GPL, for details see the file LICENSE


#include "Compilation_control.f90"

#if defined(_DARCY)
	MODULE Darcy
		use Darcy_data_types
		use Darcy_initialize_pressure
		use Darcy_initialize_saturation
		use Darcy_vtk_output
		use Darcy_xml_output
		use Darcy_lse_output
		use Darcy_grad_p
		use Darcy_pressure_solver_jacobi
		use Darcy_pressure_solver_cg
		use Darcy_pressure_solver_pipecg
		use Darcy_transport_eq
		use Darcy_permeability
		use Darcy_error_estimate
		use Darcy_adapt

		use linear_solver

		use Samoa_darcy

		implicit none

		type t_darcy
            type(t_darcy_init_pressure_traversal)           :: init_pressure
            type(t_darcy_init_saturation_traversal)         :: init_saturation
            type(t_darcy_vtk_output_traversal)              :: vtk_output
            type(t_darcy_xml_output_traversal)              :: xml_output
            type(t_darcy_lse_output_traversal)              :: lse_output
            type(t_darcy_grad_p_traversal)                  :: grad_p
            type(t_darcy_transport_eq_traversal)            :: transport_eq
            type(t_darcy_permeability_traversal)            :: permeability
            type(t_darcy_error_estimate_traversal)          :: error_estimate
            type(t_darcy_adaption_traversal)                :: adaption
            class(t_linear_solver), pointer                 :: pressure_solver

            contains

            procedure , pass :: create => darcy_create
            procedure , pass :: run => darcy_run
            procedure , pass :: destroy => darcy_destroy
        end type

		private
		public t_darcy

		contains

		!> Creates all required runtime objects for the scenario
		subroutine darcy_create(darcy, grid, l_log, i_asagi_mode)
            class(t_darcy)                                              :: darcy
 			type(t_grid), intent(inout)									:: grid
			logical, intent(in)						                    :: l_log
			integer, intent(in)											:: i_asagi_mode

			!local variables
			character (len = 64)										:: s_log_name, s_date, s_time
			integer                                                     :: i_error
            type(t_darcy_pressure_solver_jacobi)                        :: pressure_solver_jacobi
            type(t_darcy_pressure_solver_cg)                            :: pressure_solver_cg
            type(t_darcy_pressure_solver_pipecg)                        :: pressure_solver_pipecg

            !allocate solver

 			grid%r_time = 0.0_GRID_SR

            call darcy%init_pressure%create()
            call darcy%init_saturation%create()
            call darcy%vtk_output%create()
            call darcy%xml_output%create()
            call darcy%lse_output%create()
            call darcy%grad_p%create()
            call darcy%transport_eq%create()
            call darcy%permeability%create()
            call darcy%error_estimate%create()
            call darcy%adaption%create()

			call load_scenario(grid)

 			select case (cfg%i_lsolver)
                case (0)
                    call pressure_solver_jacobi%create()
                    allocate(darcy%pressure_solver, source=pressure_solver_jacobi, stat=i_error); assert_eq(i_error, 0)
                case (1)
                    call pressure_solver_cg%create()
                    call pressure_solver_cg%set_parameter(CG_RESTART_ITERS, real(cfg%i_CG_restart, SR))
                    allocate(darcy%pressure_solver, source=pressure_solver_cg, stat=i_error); assert_eq(i_error, 0)
                case (2)
                    call pressure_solver_pipecg%create()
                    call pressure_solver_pipecg%set_parameter(PCG_RESTART_ITERS, real(cfg%i_CG_restart, SR))
                    allocate(darcy%pressure_solver, source=pressure_solver_pipecg, stat=i_error); assert_eq(i_error, 0)
                case default
                    try(.false., "Invalid linear solver, must be in range 0 to 2")
            end select

            call darcy%pressure_solver%set_parameter(LS_MAX_ITERS, real(cfg%i_max_iterations, SR))

            call date_and_time(s_date, s_time)

#           if defined(_MPI)
                call mpi_bcast(s_date, len(s_date), MPI_CHARACTER, 0, MPI_COMM_WORLD, i_error); assert_eq(i_error, 0)
                call mpi_bcast(s_time, len(s_time), MPI_CHARACTER, 0, MPI_COMM_WORLD, i_error); assert_eq(i_error, 0)
#           endif

			darcy%vtk_output%s_file_stamp = trim(cfg%output_dir) // "/darcy_" // trim(s_date) // "_" // trim(s_time)
			darcy%xml_output%s_file_stamp = trim(cfg%output_dir) // "/darcy_" // trim(s_date) // "_" // trim(s_time)

			s_log_name = trim(darcy%vtk_output%s_file_stamp) // ".log"

			if (l_log) then
				_log_open_file(s_log_name)
			endif
		end subroutine

		subroutine load_scenario(grid)
			type(t_grid), intent(inout)		        :: grid

            integer                                 :: i_asagi_hints
			integer									:: i_error, i, j, i_ext_pos
			character(256)					        :: s_file_name, s_tmp
			real (kind = SR)                        :: x_min(3), x_max(3), dx(3)

#			if defined(_ASAGI)
                cfg%afh_permeability_X = asagi_grid_create(ASAGI_FLOAT)
                cfg%afh_permeability_Y = asagi_grid_create(ASAGI_FLOAT)
                cfg%afh_permeability_Z = asagi_grid_create(ASAGI_FLOAT)
                cfg%afh_porosity = asagi_grid_create(ASAGI_FLOAT)

#               if defined(_MPI)
                    call asagi_grid_set_comm(cfg%afh_permeability_X, MPI_COMM_WORLD)
                    call asagi_grid_set_comm(cfg%afh_permeability_Y, MPI_COMM_WORLD)
                    call asagi_grid_set_comm(cfg%afh_permeability_Z, MPI_COMM_WORLD)
                    call asagi_grid_set_comm(cfg%afh_porosity, MPI_COMM_WORLD)
#               endif

                call asagi_grid_set_threads(cfg%afh_permeability_X, cfg%i_threads)
                call asagi_grid_set_threads(cfg%afh_permeability_Y, cfg%i_threads)
                call asagi_grid_set_threads(cfg%afh_permeability_Z, cfg%i_threads)
                call asagi_grid_set_threads(cfg%afh_porosity, cfg%i_threads)

                !convert ASAGI mode to ASAGI parameters

                select case(cfg%i_asagi_mode)
                    case (0)
                        !i_asagi_hints = GRID_NO_HINT
                    case (1)
                        !i_asagi_hints = ieor(GRID_NOMPI, GRID_PASSTHROUGH)
                        call asagi_grid_set_param(cfg%afh_permeability_X, "grid", "pass_through")
                        call asagi_grid_set_param(cfg%afh_permeability_Y, "grid", "pass_through")
                        call asagi_grid_set_param(cfg%afh_permeability_Z, "grid", "pass_through")
                        call asagi_grid_set_param(cfg%afh_porosity, "grid", "pass_through")
                    case (2)
                        !i_asagi_hints = GRID_NOMPI
                    case (3)
                        !i_asagi_hints = ieor(GRID_NOMPI, SMALL_CACHE)
                    case (4)
                        !i_asagi_hints = GRID_LARGE_GRID
                        call asagi_grid_set_param(cfg%afh_permeability_X, "grid", "cache")
                        call asagi_grid_set_param(cfg%afh_permeability_Y, "grid", "cache")
                        call asagi_grid_set_param(cfg%afh_permeability_Z, "grid", "cache")
                        call asagi_grid_set_param(cfg%afh_porosity, "grid", "cache")
                    case default
                        try(.false., "Invalid asagi mode, must be in range 0 to 4")
                end select

                call asagi_grid_set_param(cfg%afh_permeability_X, "variable", "Kx")
                call asagi_grid_set_param(cfg%afh_permeability_Y, "variable", "Ky")
                call asagi_grid_set_param(cfg%afh_permeability_Z, "variable", "Kz")
                call asagi_grid_set_param(cfg%afh_porosity, "variable", "Phi")

                !$omp parallel private(i_error), copyin(cfg)
                    i_error = asagi_grid_open(cfg%afh_permeability_X, trim(cfg%s_permeability_file), 0); assert_eq(i_error, ASAGI_SUCCESS)
                    i_error = asagi_grid_open(cfg%afh_permeability_Y, trim(cfg%s_permeability_file), 0); assert_eq(i_error, ASAGI_SUCCESS)
                    i_error = asagi_grid_open(cfg%afh_permeability_Z, trim(cfg%s_permeability_file), 0); assert_eq(i_error, ASAGI_SUCCESS)
                    i_error = asagi_grid_open(cfg%afh_porosity, trim(cfg%s_porosity_file), 0); assert_eq(i_error, ASAGI_SUCCESS)
                !$omp end parallel

                associate(afh_perm => cfg%afh_permeability_X, afh_phi => cfg%afh_porosity)
                    x_min = [asagi_grid_min(afh_perm, 0), asagi_grid_min(afh_perm, 1), asagi_grid_min(afh_perm, 2)]
                    x_max = [asagi_grid_max(afh_perm, 0), asagi_grid_max(afh_perm, 1), asagi_grid_max(afh_perm, 2)]
                    dx = [asagi_grid_delta(afh_perm, 0), asagi_grid_delta(afh_perm, 1), asagi_grid_delta(afh_perm, 2)]

                    !HACK: round to mm to eliminate single precision errors from ASAGI(?)
                    x_min = anint(x_min * 1.0e3_SR) / 1.0e3_SR
                    x_max = anint(x_max * 1.0e3_SR) / 1.0e3_SR
                    dx = anint(dx * 1.0e3_SR) / 1.0e3_SR

                    cfg%scaling = 32.0_SR/15.0_SR * (x_max(1) - x_min(1))
                    cfg%offset = [0.5_SR * (x_min(1:2) + x_max(1:2) - cfg%scaling), x_min(3)]
                    cfg%dz = (x_max(3) - x_min(3)) / (cfg%scaling * real(max(1, _DARCY_LAYERS), SR))

                    cfg%x_min = (x_min - cfg%offset) / cfg%scaling
                    cfg%x_max = (x_max - cfg%offset) / cfg%scaling
                    cfg%dx = dx / cfg%scaling

                    !put an injection well in the center and four producers in the four corners of the domain
                    cfg%r_pos_in(:, 1) = 0.5_SR * (cfg%x_min(1:2) + cfg%x_max(1:2))
                    cfg%r_pos_prod(:, 1) = [cfg%x_min(1), cfg%x_max(2)]
                    cfg%r_pos_prod(:, 2) = [cfg%x_max(1), cfg%x_max(2)]
                    cfg%r_pos_prod(:, 3) = [cfg%x_max(1), cfg%x_min(2)]
                    cfg%r_pos_prod(:, 4) = [cfg%x_min(1), cfg%x_min(2)]

                    if (rank_MPI == 0) then
                        _log_write(1, '(" Darcy: loaded ", A, ", domain [m]: [", F0.3, ", ", F0.3, "] x [", F0.3, ", ", F0.3, "] x [", F0.3, ", ", F0.3, "]")') &
                            trim(cfg%s_permeability_file), asagi_grid_min(afh_perm, 0), asagi_grid_max(afh_perm, 0), asagi_grid_min(afh_perm, 1), asagi_grid_max(afh_perm, 1),  asagi_grid_min(afh_perm, 2), asagi_grid_max(afh_perm, 2)
                        _log_write(1, '(" Darcy:  dx [m]: [", F0.3, ", ", F0.3, ", ", F0.3, "]")') asagi_grid_delta(afh_perm, 0), asagi_grid_delta(afh_perm, 1), asagi_grid_delta(afh_perm, 2)

                        _log_write(1, '(" Darcy: loaded ", A, ", domain [m]: [", F0.3, ", ", F0.3, "] x [", F0.3, ", ", F0.3, "] x [", F0.3, ", ", F0.3, "]")') &
                            trim(cfg%s_porosity_file), asagi_grid_min(afh_phi, 0), asagi_grid_max(afh_phi, 0), asagi_grid_min(afh_phi, 1), asagi_grid_max(afh_phi, 1),  asagi_grid_min(afh_phi, 2), asagi_grid_max(afh_phi, 2)
                        _log_write(1, '(" Darcy:  dx [m]: [", F0.3, ", ", F0.3, ", ", F0.3, "]")') asagi_grid_delta(afh_phi, 0), asagi_grid_delta(afh_phi, 1), asagi_grid_delta(afh_phi, 2)

                        _log_write(1, '(" Darcy: computational domain [m]: [", F0.3, ", ", F0.3, "] x [", F0.3, ", ", F0.3, "] x [", F0.3, ", ", F0.3, "]")') cfg%offset(1), cfg%offset(1) + cfg%scaling, cfg%offset(2), cfg%offset(2) + cfg%scaling, cfg%offset(3), cfg%offset(3) + cfg%scaling * cfg%dz * max(1, _DARCY_LAYERS)
                        _log_write(1, '(" Darcy: data domain [um]: [", F0.3, ", ", F0.3, "] x [", F0.3, ", ", F0.3, "] x [", F0.3, ", ", F0.3, "]")') transpose(reshape([cfg%x_min, cfg%x_max], [3, 2]))

                        write(s_tmp, "(I0)") _DARCY_INJECTOR_WELLS
                        _log_write(1, '(" Darcy: injector positions [um]: ", ' // s_tmp // '("[", F0.3, ", ", F0.3, "] "))') cfg%r_pos_in
                        write(s_tmp, "(I0)") _DARCY_PRODUCER_WELLS
                        _log_write(1, '(" Darcy: producer positions [um]: ", ' // s_tmp // '("[", F0.3, ", ", F0.3, "] "))') cfg%r_pos_prod
                    end if
                end associate
#           else
                cfg%scaling = 1.0_SR
                cfg%offset = [0.0_SR, 0.0_SR, 0.0_SR]
                cfg%dz = 1.0_SR / real(max(1, _DARCY_LAYERS), SR)

                !remove wells from the domain
                cfg%r_pos_in = 1.5_SR
                cfg%r_pos_prod = 1.5_SR
#			endif

            !pressure is given in ppsi
            cfg%r_p_in = cfg%r_p_in * _PPSI
            cfg%r_p_prod = cfg%r_p_prod * _PPSI

            !viscosity is given in Pa * s (or cp)
            cfg%r_nu_w = cfg%r_nu_w * _PA * _S
            cfg%r_nu_n = cfg%r_nu_n * _PA * _S

            !density is given in kg/m^3 (or lb/ft^3)
            cfg%r_rho_w = cfg%r_rho_w * _KG / (_M ** 3)
            cfg%r_rho_n = cfg%r_rho_n * _KG / (_M ** 3)

            !Inflow is given in bbl/d
            cfg%r_inflow = cfg%r_inflow * _BBL / _D

#           if _DARCY_LAYERS == 0
                !In 3D, each layer has the correct height cfg%dz, in 2D the height is normed to 1.0
                !Hence, divide the inflow by the height of the domain.
                cfg%r_inflow = cfg%r_inflow / cfg%dz
#           endif

            !The well radius is given in inch
            cfg%r_well_radius = cfg%r_well_radius * _INCH

            !gravity is given in m / s^2
            cfg%g = cfg%g * _M / (_S ** 2)
		end subroutine

		!> Destroys all required runtime objects for the scenario
		subroutine darcy_destroy(darcy, grid, l_log)
            class(t_darcy)                  :: darcy
 			type(t_grid), intent(inout)     :: grid
            integer                         :: i_error
            logical		                    :: l_log

            call darcy%init_pressure%destroy()
            call darcy%init_saturation%destroy()
            call darcy%vtk_output%destroy()
            call darcy%xml_output%destroy()
            call darcy%lse_output%destroy()
            call darcy%grad_p%destroy()
            call darcy%transport_eq%destroy()
            call darcy%error_estimate%destroy()
            call darcy%permeability%destroy()
            call darcy%adaption%destroy()

            if (associated(darcy%pressure_solver)) then
                call darcy%pressure_solver%destroy()

                deallocate(darcy%pressure_solver, stat = i_error); assert_eq(i_error, 0)
            end if

			if (l_log) then
				_log_close_file()
			endif

#			if defined(_ASAGI)
				call asagi_grid_close(cfg%afh_permeability_X)
				call asagi_grid_close(cfg%afh_permeability_Y)
				call asagi_grid_close(cfg%afh_permeability_Z)
				call asagi_grid_close(cfg%afh_porosity)
#			endif
		end subroutine

		!> Sets the initial values of the scenario and runs the time steps
		subroutine darcy_run(darcy, grid)
            class(t_darcy), intent(inout)	                            :: darcy
 			type(t_grid), intent(inout)									:: grid

            integer (kind = GRID_SI)									:: i_initial_step, i_time_step, i_nle_iterations, i_lse_iterations
			real (kind = GRID_SR)										:: r_time_next_output
			type(t_grid_info)           	                            :: grid_info, grid_info_max
            integer  (kind = GRID_SI)                                   :: i_stats_phase

			!init parameters
			r_time_next_output = 0.0_GRID_SR

            if (rank_MPI == 0) then
                !$omp master
                _log_write(0, *) "Darcy: setting initial values and solving initial system.."
                _log_write(0, *) ""
                !$omp end master
            end if

            call update_stats(darcy, grid)
			i_stats_phase = 0

            i_initial_step = 0

			!set pressure initial condition
			call darcy%init_pressure%traverse(grid)

            !do some initial load balancing
			call darcy%adaption%traverse(grid)

			do
                i_nle_iterations = 1
                i_lse_iterations = 0

                call darcy%pressure_solver%set_parameter(LS_ABS_ERROR, real(cfg%r_epsilon * abs(cfg%r_p_prod - maxval(grid%p_bh)), SR))

				!reset saturation to initial condition, setup pressure equation and set refinement flags
				do
                    call darcy%init_saturation%traverse(grid)

                    !solve pressure equation

                    if (cfg%l_lse_output) then
                        call darcy%lse_output%traverse(grid)
                        call darcy%pressure_solver%solve(grid)
                        call darcy%lse_output%traverse(grid)
                    else
                        call darcy%pressure_solver%solve(grid)
                    end if

                    if (darcy%pressure_solver%get_info(LS_CUR_ITERS) == 0) then
                        exit
                    end if

                    i_lse_iterations = i_lse_iterations + darcy%pressure_solver%get_info(LS_CUR_ITERS)

                    if (rank_MPI == 0 .and. iand(i_nle_iterations, 7) == 0) then
                        !$omp master
                        _log_write(1, '(" Darcy:  coupling iters: ", I0, ", linear iters: ", I0)') i_nle_iterations, i_lse_iterations
                        !$omp end master
                    end if

                    i_nle_iterations = i_nle_iterations + 1
                end do

                if (rank_MPI == 0) then
                    grid_info%i_cells = grid%get_cells(MPI_SUM, .false.)

                    !$omp master
                    _log_write(1, '(" Darcy: adaptions: ", I0, ", coupling iters: ", I0, ", linear iters: ", I0, ", cells: ", I0)') i_initial_step, i_nle_iterations, i_lse_iterations, grid_info%i_cells
                    !$omp end master
                end if

                grid_info%i_cells = grid%get_cells(MPI_SUM, .true.)
				if (darcy%init_saturation%i_refinements_issued .le. 0 .or. i_initial_step >= 2 * cfg%i_max_depth) then
					exit
				endif

                !output grids during initial phase if and only if t_out is 0
                if (cfg%r_output_time_step == 0.0_GRID_SR) then

                    !do a dummy transport step first to determine the initial production rates
                    grid%r_dt = 0.0_SR
                    call darcy%transport_eq%traverse(grid)

                    !output grid
                    call darcy%xml_output%traverse(grid)
                    r_time_next_output = r_time_next_output + cfg%r_output_time_step
                end if

				!refine grid
				call darcy%adaption%traverse(grid)

				i_initial_step = i_initial_step + 1
			end do

            grid_info = grid%get_info(MPI_SUM, .true.)

            if (rank_MPI == 0) then
                !$omp master
                _log_write(0, *) "Darcy: done."
                _log_write(0, *) ""

                call grid_info%print()
                !$omp end master
            end if

			!output initial grid
			if (cfg%r_output_time_step >= 0.0_GRID_SR) then
                !do a dummy transport step first to determine the initial production rates
                grid%r_dt = 0.0_SR
				call darcy%transport_eq%traverse(grid)

                !output grid
				call darcy%xml_output%traverse(grid)
				r_time_next_output = r_time_next_output + cfg%r_output_time_step
			end if

			!print initial stats
			if (cfg%i_stats_phases >= 0) then
                call update_stats(darcy, grid)

                i_stats_phase = i_stats_phase + 1
			end if

            i_time_step = 0

			do
				if ((cfg%r_max_time >= 0.0 .and. grid%r_time >= cfg%r_max_time) .or. (cfg%i_max_time_steps >= 0 .and. i_time_step >= cfg%i_max_time_steps)) then
					exit
				end if

                !refine grid
                call darcy%adaption%traverse(grid)

                i_nle_iterations = 1
                i_lse_iterations = 0

                call darcy%pressure_solver%set_parameter(LS_ABS_ERROR, real(cfg%r_epsilon * abs(cfg%r_p_prod - maxval(grid%p_bh)), SR))

                do
                    !setup pressure equation
                    call darcy%permeability%traverse(grid)

                    !solve pressure equation

                    if (cfg%l_lse_output .and. mod(i_time_step, cfg%i_lse_skip + 1) == 0) then
                        call darcy%lse_output%traverse(grid)
                        call darcy%pressure_solver%solve(grid)
                        call darcy%lse_output%traverse(grid)
                    else if (mod(i_time_step, cfg%i_lse_skip + 1) == 0) then
                        call darcy%pressure_solver%solve(grid)
                    else
                        exit
                    end if

                    if (darcy%pressure_solver%get_info(LS_CUR_ITERS) == 0) then
                        exit
                    end if

                    i_lse_iterations = i_lse_iterations + darcy%pressure_solver%get_info(LS_CUR_ITERS)

                    if (rank_MPI == 0 .and. iand(i_nle_iterations, 7) == 0) then
                        !$omp master
                        _log_write(1, '(" Darcy:  coupling iters: ", I0, ", linear iters: ", I0)') i_nle_iterations, i_lse_iterations
                        !$omp end master
                    end if

                    i_nle_iterations = i_nle_iterations + 1
                end do

				!compute velocity field (to determine the time step size)
				call darcy%grad_p%traverse(grid)

				!transport equation time step
				call darcy%transport_eq%traverse(grid)
				i_time_step = i_time_step + 1

				!set refinement flags
				call darcy%error_estimate%traverse(grid)

                if (rank_MPI == 0) then
                    grid_info%i_cells = grid%get_cells(MPI_SUM, .false.)

                    !$omp master
                    _log_write(1, '(" Darcy: time step: ", I0, ", sim. time:", A, ", dt:", A, ", cells: ", I0, ", coupling iters: ", I0, ", linear iters: ", I0)') i_time_step, trim(time_to_hrt(grid%r_time)), trim(time_to_hrt(grid%r_dt)), grid_info%i_cells, i_nle_iterations, i_lse_iterations
                    !$omp end master
                end if

				!output grid
				if (cfg%r_output_time_step >= 0.0_GRID_SR .and. grid%r_time >= r_time_next_output) then
					call darcy%xml_output%traverse(grid)
					r_time_next_output = r_time_next_output + cfg%r_output_time_step
				end if

                !print stats
                if ((cfg%r_max_time >= 0.0d0 .and. grid%r_time * cfg%i_stats_phases >= i_stats_phase * cfg%r_max_time) .or. &
                    (cfg%i_max_time_steps >= 0 .and. i_time_step * cfg%i_stats_phases >= i_stats_phase * cfg%i_max_time_steps)) then
                    call update_stats(darcy, grid)

                    i_stats_phase = i_stats_phase + 1
                end if
			end do

            grid_info = grid%get_info(MPI_SUM, .true.)
            grid_info_max = grid%get_info(MPI_MAX, .true.)

            !$omp master
            if (rank_MPI == 0) then
                _log_write(0, '(" Darcy: done.")')
                _log_write(0, '()')
                _log_write(0, '("  Cells: avg: ", I0, " max: ", I0)') grid_info%i_cells / (omp_get_max_threads() * size_MPI), grid_info_max%i_cells
                _log_write(0, '()')

                call grid_info%print()
            end if
            !$omp end master
		end subroutine

		subroutine update_stats(darcy, grid)
            class(t_darcy), intent(inout)   :: darcy
 			type(t_grid), intent(inout)     :: grid

 			double precision, save          :: t_phase = huge(1.0d0)

			!$omp master
                !Initially, just start the timer and don't print anything
                if (t_phase < huge(1.0d0)) then
                    t_phase = t_phase + get_wtime()

                    call darcy%init_saturation%reduce_stats(MPI_SUM, .true.)
                    call darcy%transport_eq%reduce_stats(MPI_SUM, .true.)
                    call darcy%grad_p%reduce_stats(MPI_SUM, .true.)
                    call darcy%permeability%reduce_stats(MPI_SUM, .true.)
                    call darcy%error_estimate%reduce_stats(MPI_SUM, .true.)
                    call darcy%adaption%reduce_stats(MPI_SUM, .true.)
                    call darcy%pressure_solver%reduce_stats(MPI_SUM, .true.)
                    call grid%reduce_stats(MPI_SUM, .true.)

                    if (rank_MPI == 0) then
                        _log_write(0, *) ""
                        _log_write(0, *) "Phase statistics:"
                        _log_write(0, *) ""
                        _log_write(0, '(A, T34, A)') " Init: ", trim(darcy%init_saturation%stats%to_string())
                        _log_write(0, '(A, T34, A)') " Transport: ", trim(darcy%transport_eq%stats%to_string())
                        _log_write(0, '(A, T34, A)') " Gradient: ", trim(darcy%grad_p%stats%to_string())
                        _log_write(0, '(A, T34, A)') " Permeability: ", trim(darcy%permeability%stats%to_string())
                        _log_write(0, '(A, T34, A)') " Error Estimate: ", trim(darcy%error_estimate%stats%to_string())
                        _log_write(0, '(A, T34, A)') " Adaptions: ", trim(darcy%adaption%stats%to_string())
                        _log_write(0, '(A, T34, A)') " Pressure Solver: ", trim(darcy%pressure_solver%stats%to_string())
                        _log_write(0, '(A, T34, A)') " Grid: ", trim(grid%stats%to_string())
                        _log_write(0, '(A, T34, F12.4, A)') " Element throughput: ", 1.0d-6 * dble(grid%stats%i_traversed_cells) / t_phase, " M/s"
                        _log_write(0, '(A, T34, F12.4, A)') " Memory throughput: ", dble(grid%stats%i_traversed_memory) / ((1024 * 1024 * 1024) * t_phase), " GB/s"
                        _log_write(0, '(A, T34, F12.4, A)') " Asagi time:", grid%stats%r_asagi_time, " s"
                        _log_write(0, '(A, T34, F12.4, A)') " Phase time:", t_phase, " s"
                        _log_write(0, *) ""
                    end if
                end if

                call darcy%init_saturation%clear_stats()
                call darcy%transport_eq%clear_stats()
                call darcy%grad_p%clear_stats()
                call darcy%permeability%clear_stats()
                call darcy%error_estimate%clear_stats()
                call darcy%adaption%clear_stats()
                call darcy%pressure_solver%clear_stats()
                call grid%clear_stats()

                t_phase = -get_wtime()
            !$omp end master
        end subroutine
	END MODULE Darcy
#endif
