<h1>Jmeter Cloud</h1>

Runs a Jmeter load test in the cloud. Achieves 3 objectives:
1. Creates an AWS instance. 
2. Runs jmeter in that instance
3. Downloads the result log files to your machine

**Caveats**: 

1. Make sure you have a Jmeter (.jmx) test plan  
2. Make sure you have a valid key pair .pem file 
3. Make sure you have aws-okta configured
4. Make sure you run this in aws-okta nordstrom federated bash
5. If you're using CSV Data Config, make sure your csv is in the same directory as .jmx file and specify relative path in .jmx file.

<h3> Quick Link(s): </h3>

*  [Packge Usage and more info.](https://github.com/KirtimanS/Jmeter-Cloud/wiki) - read about how to use the package and how to avoid common pitfalls

<h2>Getting Started</h2>
<h3>Prerequisites</h3>

*  <b>Python 3.6+:</b> Most Macs and Linux distributions come with Python 2.7 installed. To install and use python 3.6+ see this: [Installing Python3](https://realpython.com/installing-python/). Or you can use Homebrew.
*  <b>Boto3:</b> `pip install Boto3` Further documentation : [Install Boto3](https://pypi.org/project/boto3/)
*  <b>Paramiko:</b> `pip install paramiko` Paramiko homepage: [Install Paramiko](http://www.paramiko.org/)
*  <b>Pip:</b> If you installed Python3.6+ already you should have associated pip installed. If not then see this: [Installing Pip](https://pip.pypa.io/en/stable/installing/)

<h3>Installing</h3>

Simply clone the source project and unzip it. 

<h3>Local Deployment</h3>

1. Install the prerequisities
2. Go to the project Source Directory
3. Open a terminal
4. Navigate to the folder where you saved this project
5. Make sure you're in nordstrom federated aws-cli (Look at the __Common Gotchas__ wiki link above.)
6. Run Setup.py (fail safe incase you don't have all prereqs)
7. There are two ways to run this:
    1. Go up one level (from project directory) and `python jmeter_cloud` (Assuming project is saved as __jmeter_cloud__ directory and Python3 is installed with __python__ command)
    2. Or `python __main__.py` 
8. Add testplan path, key pair path and other arguments as shown in the __package usage__ in the wiki.

<h2> Results </h2>

1. Mirrors the ec2 instance terminal in real-time after each command is passed. 
2. Runs the load test using user provided jmeter (.jmx) config, key pair (.pem) and other neccessary files.
3. Shows the non-GUI Jmeter terminal info. 
4. Dowloads load test result files (.jtl) and jmeter logs (.log) with the prefix: `<testplan file name>_<current time in format: %Y-%m-%d %H:%M:%S>_`
    1. Example Result log (.jtl) file name: "*myTestPlan_2020-02-12 13/30/56_log.jtl*"
    2. Example Jmeter Log (.log) file name: "*myTestPlan_2020-02-12 13/30/56_jmeter.log*"

<h2> Future Work </h2>

1. Work on a distribution package
2. Add support for GCP and Azure
3. Work on Dasboard (grafana etc.) for displaying .jtl log results
4. Work on Factory Pattern
5. Add SSM support

<h3> Author(s) </h3>

*  Kirtiman Sinha - 2/05 - 2/08 (2020)
