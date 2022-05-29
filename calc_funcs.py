from scapy.all import *
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_pcap(pcap_name):
    scapy_cap = rdpcap(pcap_name)
    print('Read ', pcap_name, '. Total Packets: ', len(scapy_cap))
    return scapy_cap

def create_if_not_present_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def filter_pcap(scapy_cap=None, src_ip=None, src_port=None, dest_ip=None, dest_port=None):
    filtered = []
    if scapy_cap:
        for pkt in scapy_cap:
            if IP in pkt and TCP in pkt:
                if pkt.len > 1400:
                    if src_ip:
                        if pkt[IP].src != src_ip:
                            continue
                    if src_port:
                        if pkt[TCP].sport != src_port:
                            continue
                    if dest_ip:
                        if pkt[IP].dst != dest_ip:
                            continue
                    if dest_port:
                        if pkt[TCP].dport != dest_port:
                            continue
                    filtered.append(pkt)
    print('After Filtering No. of Packets: ', len(filtered))
    return filtered

def get_pkt_seq_n_time(scapy_cap):
    seq_time_list = []
    for pkt in scapy_cap:
        seq_time_list.append((pkt[TCP].seq, float(pkt.time)))
    print('Fetched sequence number and timestamp')
    return seq_time_list

def save_pcap(pkt_list, name):
    print('Saved as pcap: ', name)
    wrpcap(name, pkt_list)

def most_common(lst):
    return max(set(lst), key=lst.count)

def remove_NaN(pandas_df):
    for column in pandas_df.columns:
        pandas_df = pandas_df[pandas_df[column].notna()]
    print('Removed NaN from columns.')
    return pandas_df

def get_src_port(scapy_cap):
    src_port_list = []
    for pkt in scapy_cap:
        if TCP in pkt:
            src_port_list.append(pkt[TCP].sport)
    src_port = most_common(src_port_list)
    print('Source Port is: ', src_port)
    return src_port

def draw_hist(data_arr, bins='auto', yscale='log', hist_filename='histogram.jpg'):    
    plt_hist = plt
    plt_hist.yscale(yscale)
    plt_hist.xlabel('Delay(ms) (min: ' + str(round(data_arr.min(), 3)) + 'ms max: ' + str(round(data_arr.max(), 3)) + 'ms)')
    plt_hist.ylabel('Frequency')
    plt_hist.hist(data_arr, bins=bins)
    plt_hist.savefig(hist_filename)
    plt_hist.close()
    if data_arr.max() > 20:
        plt_hist = plt
        plt_hist.yscale(yscale)
        plt_hist.xlabel('Delay(ms)')
        plt_hist.ylabel('Frequency')
        plt_hist.xlim([data_arr.min(), data_arr.min() + 10])
        plt_hist.hist(data_arr, bins=bins)
        plt_hist.savefig(hist_filename.split('.')[0] + '_zoomed.' + hist_filename.split('.')[1])
        plt_hist.close()

def draw_pdf(data_arr, color='red', label='PDF', bins='auto', pdf_filename='pdf.jpg'):
    count, bins_count = np.histogram(data_arr, bins=bins)
    pdf = count / sum(count)
    plt_pdf = plt
    plt_pdf.xlabel('Delay(ms)')
    plt_pdf.ylabel('PDF')
    plt_pdf.axhline(y = 0.0, color = 'r', linestyle = '-')
    plt_pdf.plot(bins_count[1:], pdf, color=color, label='PDF')
    plt_pdf.savefig(pdf_filename)
    plt_pdf.close()
    if data_arr.max() > 20:
        plt_pdf = plt
        plt_pdf.xlabel('Delay(ms)')
        plt_pdf.ylabel('PDF')
        plt_pdf.xlim([data_arr.min(), data_arr.min() + 10])
        plt_pdf.axhline(y = 0.0, color = 'r', linestyle = '-')
        plt_pdf.plot(bins_count[1:], pdf, color=color, label='PDF')
        plt_pdf.savefig(pdf_filename.split('.')[0] + '_zoomed.' + pdf_filename.split('.')[1])
        plt_pdf.close()

def draw_cdf(data_arr, color='blue', label='CDF', bins='auto', cdf_filename='cdf.jpg'):
    count, bins_count = np.histogram(data_arr, bins=bins)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt_cdf = plt
    plt_cdf.xlabel('Delay(ms)')
    plt_cdf.ylabel('CDF')
    plt_cdf.axhline(y = 1.0, color = 'r', linestyle = '-')
    plt_cdf.plot(bins_count[1:], cdf, color=color, label="CDF")
    plt_cdf.savefig(cdf_filename)
    plt_cdf.close()
    if data_arr.max() > 20:
        plt_cdf = plt
        plt_cdf.xlabel('Delay(ms)')
        plt_cdf.ylabel('CDF')
        plt_cdf.xlim([data_arr.min(), data_arr.min() + 10])
        plt_cdf.axhline(y = 1.0, color = 'r', linestyle = '-')
        plt_cdf.plot(bins_count[1:], cdf, color=color, label="CDF")
        plt_cdf.savefig(cdf_filename.split('.')[0] + '_zoomed.' + cdf_filename.split('.')[1])
        plt_cdf.close()

def draw_pdf_cdf(data_arr, pdf_color='red', cdf_color='blue', bins='auto', pdf_cdf_filename='pdf_cdf.jpg'):
    count, bins_count = np.histogram(data_arr, bins=bins)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Delay(ms)')
    ax1.set_ylabel('PDF')
    ax1.plot(bins_count[1:], pdf, color=pdf_color, label='PDF')
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('CDF')
    ax2.plot(bins_count[1:], cdf, color=cdf_color, label='CDF')
    ax2.tick_params(axis='y', labelcolor=color)
    plt.savefig(pdf_cdf_filename)
    plt.close()
    if data_arr.max() > 20:
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        plt.xlim([data_arr.min(), data_arr.min() + 10])
        ax1.set_xlabel('Delay(ms)')
        ax1.set_ylabel('PDF')
        ax1.plot(bins_count[1:], pdf, color=pdf_color, label='PDF')
        ax1.tick_params(axis='y', labelcolor=color)
        ax2 = ax1.twinx()
        color = 'tab:blue'
        ax2.set_ylabel('CDF')
        ax2.plot(bins_count[1:], cdf, color=cdf_color, label='CDF')
        ax2.tick_params(axis='y', labelcolor=color)
        plt.savefig(pdf_cdf_filename.split('.')[0] + '_zoomed.' + pdf_cdf_filename.split('.')[1])
        plt.close()
