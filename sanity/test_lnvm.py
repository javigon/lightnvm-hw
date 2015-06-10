import os
import time
import subprocess
import getopt
import argparse

FIO_IOPS_POS = 7
FIO_SLAT_POS = 9
FIO_CLAT_POS_START = 13
FIO_LAT_POS_START = 37

KERNEL_VERSION = os.uname()[2]
FIO_M_COLUMNS = ("iotype;bs;njobs;iodepth;iops;slatmin;slatmax;slatavg;clatmin;"
                                        "clatmax;clatavg;latmin;latmax;latavg")

# Default parameters (modifiable from input arguments)
fio_ioengine = 'libaio'
fio_num_jobs = '1'
fio_size = '1G'
fio_io_depth = '1'
fio_block_size = '4k'
fio_runtime = '60'
fio_exe = 'sudo fio -- minimal'
fio_force = ''

# LightNVM configuration (modifiable from input arguments)
lnvm_device = 'nullb0'
lnvm_target = 'sanity'
lnvm_file = '/dev/' + lvnm_device
lnvm_config = '/sys/block/' + lvnm_device + 'lightnvm/configure'
lnvm_remove = '/sys/block/' + lvnm_device + 'lightnvm/remove'
lnvm_config_cmd = ("sudo sh -c 'echo \"rrpc " + lnvm_target + "0:0\" > " +
                                                            lnvm_config + "''")

def generated(args):
    fio_template = 'sanity/sanity.fio'
    for run in ('write', 'randwrite', 'read', 'randread'):
        for blocksize in ('512', '1k', '4k', '512k'):
            for numjobs in (1, 32, 64):
                for iodepth in (1, 8, 32, 64, 128):
                    fio_type_offset = 0
                    iops = 0.0
                    slat = [0.0 for i in range(3)]
                    clat = [0.0 for i in range(3)]
                    lat = [0.0 for i in range(3)]

                    result = ("" + str(run) + ";" + str(blocksize) + ";" +
                                        str(numjobs) + ";" + str(iodepth) + ";")

                    #Assign system variables for current fio test
                    os.environ['FILENAME'] = lnvm_file
                    os.environ['SIZE'] = fio_size
                    os.environ['NUM_JOBS'] = fio_num_jobs
                    os.environ['IO_DEPTH'] = fio_io_depth
                    os.environ['BLOCK_SIZE'] = fio_block_size
                    os.environ['RUNTIME'] = fio_runtime
                    os.environ['IOENGINE'] = fio_ioengine

                    # TODO: Get fio command from fio template and parse it here
                    command = fio_exe + ' ' + fio_template
                    # command = "sudo fio --minimal -name=temp-fio --bs=" +
                            # str(blocksize) + " --ioengine=libaio --iodepth=" +
                            # str(iodepth) + " --size=" + fio_size +
                            # " --direct=1 --rw="+str(run) +
                            # " --filename=/dev/"+str(device) +
                            # " --numjobs="+str(numjobs) +
                            # " --time_based --runtime=" +
                            # fio_runtime + " --group_reporting"
                    print (command)

                    if not os.path.exists(lnvm_config):
                        print ("lnvm_test: Device " + lnvm_device +
                                                            " does not exist!")

                    if not os.path.exists(lnvm_file):
                        print lnvm_config_cmd
                        # subprocess.check_output()

                    # subprocess.check_output(command, shell=True)

                    # for i in range (0, n_iterations):
                    #     os.system("sleep 2") #Give time to finish inflight IOs
                    #     output = subprocess.check_output(command, shell=True)
                    #     if "write" in run:
                    #         fio_type_offset=41
                    #
                    #     # fio is called with --group_reporting. This means that all
                    #     # statistics are group for different jobs.
                    #
                    #     # iops
                    #     iops = iops + float(output.split(";")[fio_type_offset +
                    #                                             fio_iops_pos])
                    #
                    #     # slat
                    #     for j in range (0, 3):
                    #         slat[j] = slat[j] + float(output.split(";")
                    #                     [fio_type_offset+fio_slat_pos_start+j])
                    #     # clat
                    #     for j in range (0, 3):
                    #         clat[j] = clat[j] + float(output.split(";")
                    #                     [fio_type_offset+fio_clat_pos_start+j])
                    #     # lat
                    #     for j in range (0, 3):
                    #         lat[j] = lat[j] + float(output.split(";")
                    #                     [fio_type_offset+fio_lat_pos_start+j])
                    #
                    # # iops
                    # result = result+str(iops / n_iterations)
                    # # slat
                    # for i in range (0, 3):
                    #     result = result+";"+str(slat[i] / n_iterations)
                    # # clat
                    # for i in range (0, 3):
                    #     result = result+";"+str(clat[i] / n_iterations)
                    # # lat
                    # for i in range (0, 3):
                    #     result = result+";"+str(lat[i] / n_iterations)
                    #
                    # print (result)
                    #
def custom(args):
    print "Adios mundo"

def scripts(args):
    print "Ahhh mundo"

def all(args):
    print "Hola mundo"
    print "Adios mundo"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=
        'Test LightNVM-enabled device using flexible I/O tester (fio).')
    parser.add_argument('-g', '--generated', dest='action', action='store_const',
                        const=generated, help='Execute generated fio tests.')
    parser.add_argument('-c', '--custom', dest='action', action='store_const',
                        const=custom, help='Execute custom fio tests.')
    parser.add_argument('-s', '--scripts', dest='action', action='store_const',
                        const=scripts, help='Execute fio scripts in fio_tests/')
    parser.add_argument('-a', '--all', dest='action', action='store_const',
                        const=all, help='Execute all fio tests.')

    #TODO: Add argument to execute minimal or complete fio
    #TODO: Add argument to produce output file
    #TODO: Add argument to specific n of iterations (default 3?)

    args = parser.parse_args()
    if args.action is None:
        parser.parse_args(['-h'])
    args.action(args)
