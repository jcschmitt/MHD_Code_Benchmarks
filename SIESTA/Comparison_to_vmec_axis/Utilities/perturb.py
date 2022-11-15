import argparse
from omfit_classes.omfit_namelist import OMFITnamelist
import subprocess
import netCDF4

#-------------------------------------------------------------------------------
#  Perturb the restart file and restart the equilibrium.
#
#  param[in] namelist      Siesta namelist object.
#  param[in] num_processes Number of processes to run Siesta with.
#  param[in] radius        Radial index.
#  param[in] m_mode        Poloidal mode.
#  param[in] n_mode        Toroidal mode.
#  param[in] quantity      Quantity name to check.
#  param[in] perturbation  Perturbation change the fourier mode to.
#-------------------------------------------------------------------------------
def perturb_siesta(namelist, num_processes, radius, m_mode, n_mode, quantity, perturbation):
    namelist['SIESTA_INFO']['NITER'] = 1000000
    namelist['SIESTA_INFO']['LRESTART'] = True

    namelist.save()

    restart_file = 'siesta_{}.nc'.format(namelist['SIESTA_INFO']['RESTART_EXT'])

    with netCDF4.Dataset(restart_file, 'a') as nc_ref:
        nc_ref.variables[quantity][radius - 1, n_mode + namelist['SIESTA_INFO']['NTORIN'], m_mode] = perturbation*nc_ref.variables[quantity][radius - 1, n_mode + namelist['SIESTA_INFO']['NTORIN'], m_mode]

    subprocess.run(['mpirun', '-n', '{}'.format(num_processes), 'xsiesta'])

#-------------------------------------------------------------------------------
#  Initialize SIESTA.
#
#  param[in] namelist      Siesta namelist object.
#  param[in] num_processes Number of processes to run Siesta with.
#-------------------------------------------------------------------------------
def init_siesta(namelist, num_processes):
    namelist['SIESTA_INFO']['NITER'] = 1
    namelist['SIESTA_INFO']['LRESTART'] = False
    
    namelist.save()
    
    subprocess.run(['mpirun', '-n', '{}'.format(num_processes), 'xsiesta'])

#-------------------------------------------------------------------------------
#  Load the siesta namelist input.
#
#  param[in] namelist Siesta namelist object.
#  param[in] radius   Radial index.
#  param[in] m_mode   Poloidal mode.
#  param[in] n_mode   Toroidal mode.
#-------------------------------------------------------------------------------
def check_modes(namelist, radius, m_mode, n_mode):
    if (radius < 1 and radius > namelist['SIESTA_INFO']['NSIN'] + namelist['SIESTA_INFO']['NSIN_EXT']):
        print('s_index {} out of range (1:{}).'.format(radius, namelist['SIESTA_INFO']['NSIN'] + namelist['SIESTA_INFO']['NSIN_EXT']))
        exit(1)
    elif (m_mode < -namelist['SIESTA_INFO']['MPOLIN'] and m_mode > namelist['SIESTA_INFO']['MPOLIN']):
        print('m_mode {} out of range ({}:{}).'.format(m_mode, -namelist['SIESTA_INFO']['MPOLIN'], namelist['SIESTA_INFO']['MPOLIN']))
        exit(1)
    elif (n_mode < -namelist['SIESTA_INFO']['NTORIN'] and n_mode > namelist['SIESTA_INFO']['NTORIN']):
        print('n_mode {} out of range ({}:{}).'.format(m_mode, -namelist['SIESTA_INFO']['NTORIN'], namelist['SIESTA_INFO']['NTORIN']))
        exit(1)

#-------------------------------------------------------------------------------
#  Check if the quantity that's being perturbed is valid.
#
#  param[in] quantity Quantity name to check.
#-------------------------------------------------------------------------------
def check_quantity(quantity):
    if (not(quantity == 'jpresch_m_n_r_'  or
            quantity == 'jpressh_m_n_r_'  or
            quantity == 'jBsupssh_m_n_r_' or
            quantity == 'jBsupsch_m_n_r_' or
            quantity == 'jBsupuch_m_n_r_' or
            quantity == 'jBsupush_m_n_r_' or
            quantity == 'jBsupvch_m_n_r_' or
            quantity == 'jBsupvsh_m_n_r_')):
        print('Quantity {} is invalid.'.format(quantity))
        exit(1)

#-------------------------------------------------------------------------------
#  Parse Command Line Arguments
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    command_line_parser = argparse.ArgumentParser()
    command_line_parser.add_argument('-nl',
                                     '--name_list_file',
                                     required=False,
                                     action='store',
                                     dest='namelist_file',
                                     help='Name of the SIESTA namelist input.',
                                     default='siesta.jcf',
                                     metavar='NAMELIST_FILE')
    command_line_parser.add_argument('-s',
                                     '--s_index',
                                     required=True,
                                     action='store',
                                     dest='s_index',
                                     type=int,
                                     help='Radial Index',
                                     metavar='S_INDEX')
    command_line_parser.add_argument('-m',
                                     '--mpol_mode',
                                     required=True,
                                     action='store',
                                     dest='mpol_mode',
                                     type=int,
                                     help='Poloidal Mode Number',
                                     metavar='MPOL_MODE')
    command_line_parser.add_argument('-n',
                                     '--ntor_mode',
                                     required=True,
                                     action='store',
                                     dest='ntor_mode',
                                     type=int,
                                     help='Toroidal Mode Number',
                                     metavar='NTOR_MODE')
    command_line_parser.add_argument('-p',
                                     '--perturbation',
                                     required=True,
                                     action='store',
                                     dest='perturbation',
                                     type=float,
                                     help='Perturbation value for the mode.',
                                     metavar='PERTURBATION')
    command_line_parser.add_argument('-q',
                                     '--quantity',
                                     required=True,
                                     action='store',
                                     dest='quantity',
                                     help='Qunatity to change',
                                     metavar='QUANTITY')
    command_line_parser.add_argument('-np',
                                     '--num_processes',
                                     required=True,
                                     action='store',
                                     dest='num_processes',
                                     type=int,
                                     help='Qunatity to change',
                                     metavar='Number of processors to run SIESTA on.')

    args = vars(command_line_parser.parse_args())

#  Remove empty arguments.
    for key in [key for key in args if args[key] == None]:
        del args[key]

    check_quantity(args['quantity'])

    namelist = OMFITnamelist(args['namelist_file'])
    if 'NSIN_EXT' not in namelist['SIESTA_INFO']:
        namelist['SIESTA_INFO']['NSIN_EXT'] = 0

    check_modes(namelist, args['s_index'], args['mpol_mode'], args['ntor_mode'])

    init_siesta(namelist, args['num_processes'])
    perturb_siesta(namelist, args['num_processes'], args['s_index'], args['mpol_mode'], args['ntor_mode'], args['quantity'], args['perturbation'])
