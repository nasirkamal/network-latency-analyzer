import argparse
from wsgiref.simple_server import WSGIRequestHandler
from calc_funcs import *

args_parser = argparse.ArgumentParser()
args_parser.add_argument('--sender_pcap', '-sp', type=str, required=True, help='Pcap from the node sending traffic.')
args_parser.add_argument('--receiver_pcap', '-rp', type=str, required=True, help='Pcap from the node receiving traffic.')
args_parser.add_argument('--sender_ip', '-sip', type=str, required=True, help='IP address of the sender node.')
args_parser.add_argument('--receiver_ip', '-rip', required=True, help='IP address of the receiver node.')
args_parser.add_argument('--dest_port', '-dp', type=int, required=False, default=5201, help='Listening server port, in case of iperf3 5201.')
args_parser.add_argument('--name', '-n', type=str, required=False, default='noname', help='Name of the experiment to generate graphs with that name for distiction.')
args_parser.add_argument('--hist_filename', '-hf', type=str, required=False, help='File name to save histogram of packet delays. E.g., hist.jpg')
args_parser.add_argument('--pdf_filename', '-pf', type=str, required=False, help='File name to save pdf graph. E.g., pdf.jpg')
args_parser.add_argument('--cdf_filename', '-cf', type=str, required=False, help='File name to save cdf graph. E.g., cdf.jpg')
args_parser.add_argument('--pdf_cdf_filename', '-pcf', type=str, required=False, help='File name to save pdf-cdf graph. E.g., pdf-cdf.jpg')
args_parser.add_argument('--bins', '-bn', default='auto', required=False, help='Number of bins for drawing histogram/pdf/cdf.')
args_parser.add_argument('--hist_yscale', '-hy', default='linear', required=False, type=str, choices=['linear', 'log', 'symlog', 'logit'], help='Histogram Y-Scale, ')
args_parser.add_argument('--pcaps_dir', '-pd', default='pcaps', required=False, type=str, help='Directory name containing pcaps.')
args_parser.add_argument('--graphs_dir', '-gd', default='graphs', required=False, type=str, help='Directory name to save graph plots output.')

args = args_parser.parse_args()

if __name__ == '__main__':
    if args.hist_filename:
        hist_filename = os.path.join(args.graphs_dir, args.hist_filename)
    else:
        hist_filename = os.path.join(args.graphs_dir, args.name, args.name + '_histogram.jpg')

    if args.pdf_filename:
        pdf_filename = os.path.join(args.graphs_dir, args.pdf_filename)
    else:
        pdf_filename = os.path.join(args.graphs_dir, args.name, args.name + '_pdf.jpg')

    if args.cdf_filename:
        cdf_filename = os.path.join(args.graphs_dir, args.cdf_filename)
    else:
        cdf_filename = os.path.join(args.graphs_dir, args.name, args.name + '_cdf.jpg')

    if args.pdf_cdf_filename:
        pdf_cdf_filename = os.path.join(args.graphs_dir, args.pdf_cdf_filename)
    else:
        pdf_cdf_filename = os.path.join(args.graphs_dir, args.name, args.name + '_pdf_cdf.jpg')

    create_if_not_present_dir(args.graphs_dir)
    graphs_save_dir = os.path.join(args.graphs_dir, args.name)
    create_if_not_present_dir(graphs_save_dir)

    sender_pcap_filename = os.path.join(args.pcaps_dir, args.sender_pcap)
    receiver_pcap_filename = os.path.join(args.pcaps_dir, args.receiver_pcap)

    sender_scapy_cap = read_pcap(sender_pcap_filename)
    receiver_scapy_cap = read_pcap(receiver_pcap_filename)
    
    ip_filtered_sender_scapy_cap = filter_pcap(scapy_cap=sender_scapy_cap, src_ip=args.sender_ip, dest_ip=args.receiver_ip)
    ip_filtered_receiver_scapy_cap = filter_pcap(scapy_cap=receiver_scapy_cap, src_ip=args.sender_ip, dest_ip=args.receiver_ip)

    src_port = get_src_port(ip_filtered_sender_scapy_cap)

    sender_filtered_scapy_cap = filter_pcap(scapy_cap=ip_filtered_sender_scapy_cap, src_port=src_port, dest_port=args.dest_port)
    receiver_filtered_scapy_cap = filter_pcap(scapy_cap=ip_filtered_receiver_scapy_cap, src_port=src_port, dest_port=args.dest_port)

    sender_seq_time_list = get_pkt_seq_n_time(sender_filtered_scapy_cap)
    receiver_seq_time_list = get_pkt_seq_n_time(receiver_filtered_scapy_cap)

    sender_df = pd.DataFrame(sender_seq_time_list, columns =['Sequence', 'Time_Transmit'])
    receiver_df = pd.DataFrame(receiver_seq_time_list, columns =['Sequence', 'Time_Receive'])

    sender_df.drop_duplicates(subset ="Sequence", keep = 'last', inplace = True)
    receiver_df.drop_duplicates(subset ="Sequence", keep = 'last', inplace = True)

    final_df = pd.merge(sender_df, receiver_df, on='Sequence', how='outer')
    final_df = remove_NaN(final_df)

    final_df['Delay'] = (final_df['Time_Receive'] - final_df['Time_Transmit']) * 1000
    data_arr = final_df['Delay'].to_numpy()


    draw_hist(data_arr, bins=args.bins, yscale=args.hist_yscale, hist_filename=hist_filename)
    draw_pdf(data_arr, bins=args.bins, pdf_filename=pdf_filename)
    draw_cdf(data_arr, bins=args.bins, cdf_filename=cdf_filename)
    draw_pdf_cdf(data_arr, bins=args.bins, pdf_cdf_filename=pdf_cdf_filename)
