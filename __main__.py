import argparse
import core

parser = argparse.ArgumentParser(description='Start JMeter load test in an AWS instance.')
parser.add_argument('--tplan', '--testPlan', required=True, dest='test_plan', metavar='\b', help='complete path to a JMeter testplan')
parser.add_argument('--k', '--keyPair', required=True, dest='key', metavar='\b', help='complete path to KeyPair used to connect to created ec2')
parser.add_argument('--t', '--threads', dest='threads', metavar='\b', help='threads or virtual users hitting the endpoint')
parser.add_argument('--iter', '--iterations', dest='iter', metavar='\b', help='number of iterations for load test')
parser.add_argument('--a', '--ami', dest='ami', metavar='\b', default='ami-04590e7389a6e577c', help='imageId for the instance ami.')
parser.add_argument('--c', '--csv', metavar='\b', dest='csv', help='complete path of CSV file to use with CSV Config. Required if you are using CSV config in testplan')
parser.add_argument('--l', '--log', metavar='\b', dest='log', default='log.jtl', help='file name for .jtl log generated and downloaded to your machine after running load test (default: log.jtl)')
parser.add_argument('--ins', '--instanceType', metavar='\b', dest='instance', default='t2.medium', help='instance type to run the load test (default=t2.medium)')
parser.add_argument('--r', '--region', metavar='\b', dest='region', default='us-west-2', help='aws region where ec2 instance is to be deployed')
parser.add_argument('--d', '--delIns', metavar='\b', dest='del_ins', default='Y', choices=['Yes', 'No', 'Y', 'N', 'y', 'n', 'yes', 'no'], help='delete AWS instance at the end (Y, N)')

args = parser.parse_args()

def main():
	core_runner = core.Core(args)
	core_runner.run()


if __name__ == '__main__':
	main()
