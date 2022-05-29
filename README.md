# network-latency-analyzer
Python Code to Analyze Network Latency Using Packet Capture Between Precisely Synchronized Nodes.

To use the code some python3 and some python3 packages are required.To install required packages run:
```bash
pip3 install -r requirements.txt
```
to analyze the pcaps e.g., sender.pcap and receiver.pcap generated from nodes having IP addresses 10.10.10.1 and 10.10.10.2 respectively run the following command:
```bash
python3 analyze.py -sp sender.pcap -rp receiver.pcap -hy log -n experiment_1 -sip 10.10.10.1 -rip 10.10.10.2
```
The code will generate histogram of latencies (in miliseconds).

Script help is available with -h flag.
```bash
python3 analyze.py -h
```
```python
optional arguments:
  -h, --help            show this help message and exit
  --sender_pcap SENDER_PCAP, -sp SENDER_PCAP
                        Pcap from the node sending traffic.
  --receiver_pcap RECEIVER_PCAP, -rp RECEIVER_PCAP
                        Pcap from the node receiving traffic.
  --sender_ip SENDER_IP, -sip SENDER_IP
                        IP address of the sender node.
  --receiver_ip RECEIVER_IP, -rip RECEIVER_IP
                        IP address of the receiver node.
  --dest_port DEST_PORT, -dp DEST_PORT
                        Listening server port, in case of iperf3 5201.
  --name NAME, -n NAME  Name of the experiment to generate graphs with that
                        name for distiction.
  --hist_filename HIST_FILENAME, -hf HIST_FILENAME
                        File name to save histogram of packet delays. E.g.,
                        hist.jpg
  --pdf_filename PDF_FILENAME, -pf PDF_FILENAME
                        File name to save pdf graph. E.g., pdf.jpg
  --cdf_filename CDF_FILENAME, -cf CDF_FILENAME
                        File name to save cdf graph. E.g., cdf.jpg
  --pdf_cdf_filename PDF_CDF_FILENAME, -pcf PDF_CDF_FILENAME
                        File name to save pdf-cdf graph. E.g., pdf-cdf.jpg
  --bins BINS, -bn BINS
                        Number of bins for drawing histogram/pdf/cdf.
  --hist_yscale {linear,log,symlog,logit}, -hy {linear,log,symlog,logit}
                        Histogram Y-Scale,
  --pcaps_dir PCAPS_DIR, -pd PCAPS_DIR
                        Directory name containing pcaps.
  --graphs_dir GRAPHS_DIR, -gd GRAPHS_DIR
 ```
