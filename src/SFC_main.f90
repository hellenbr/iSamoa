! Sam(oa)² - SFCs and Adaptive Meshes for Oceanic And Other Applications
! Copyright (C) 2010 Oliver Meister, Kaveh Rahnema
! This program is licensed under the GPL, for details see the file LICENSE


#include "Compilation_control.f90"

PROGRAM samoa
	USE SFC_traversal

	implicit none

    !init MPI
    call init_mpi()

    !read config from program arguments and print it out
    call cfg%read_from_program_arguments()

    ! This info should only be printed once at the beginning of launch
    ! Need to prevent JOINING ranks from polluting the output
    if (is_root()) then
		call cfg%print()
    end if

#	if defined(_IMPI_NODES)
	call get_node_id(trim(cfg%s_impi_host_file))
#	endif

    !init element transformation data
    call init_transform_data()

    !run scenario selector
    call sfc_generic()

    !finalize MPI
    call finalize_mpi()

	stop
end PROGRAM samoa
