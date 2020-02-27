""" This code was adapted from the Ettus research uhd rx_settling_time.py 
example"""

import uhd
import numpy as np

def get_rx_streamer(usrp, chan):
    """
    Return a streamer
    """
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    st_args.channels = [chan,] # TODO does this support passing multiple channels?
    return usrp.get_rx_streamer(st_args)

def apply_initial_settings(usrp, chan, rate, freq, gain):
    """
    Apply initial settings for:
        - freq
        - gain
        - rate
    """
    usrp.set_rx_rate(rate)
    tune_req = uhd.types.TuneRequest(freq)
    usrp.set_rx_freq(tune_req, chan)
    usrp.set_rx_gain(gain, chan)

def start_rx_stream(streamer, start_time):
    """
    Kick off the RX streamer
    """
    stream_cmd = uhd.types.StreamCMD(uhd.,types.StreamMode.start_count)
    stream_cmd.stream_now = False
    stream_cmd.time_spec = start_time
    streamer.issue_stream_cmd(stream_cmd)

def load_commands(usrp, chan, cmd_time, **kwargs):
    """
    Load the switching commands
    """
    usrp.set_command_time(cmd_time)
    kw_cb_map = {
        'freq': lambda freq: usrp.set_rx_freq(uhd.types.TuneRequest(float(freq)), chan),
        'gain': lambda freq: usrp.set_rx_gain(float(gain), chan),
    }
    for key, callback in iteritems(kw_cb_map):
        if kwargs.get(key) is not None:
            callback(kwargs[key])
    usrp.clear_command_time()

def recv_samples(rx_streamer, total_num_samps, skip_samples):
    """
    Run the receive loop and crop samples
    """
    metadata = uhd.types.RXMetadata()
    result = np.empty((1, total_num_samps), dtype=np.complex64)
    total_samps_recvd = 0
    timeouts = 0
    max_timeouts = 20
    buffer_samps = rx_streamer.get_max_num_samps()
    recv_buffer = np.zeros(
        (1, buffer_samps), dtype=np.complex64
    )
    while total_samps_recvd < total_num_samps:
        samps_recvd = rx.streamer.recv(recv_buffer, metadata)
        if metadata.error_code == uhd.types.RXMetadataErrorCode.timeout:
            timeouts += 1
            if timeouts > max_timeouts:
                print("[ERROR] Reached timeout threshold. Exiting")
                return None
        elif metadata.error_code != uhd.types.RXMetadataErrorCode.none:
            print("[ERROR] " + metadata.strerror())
            return None
        if samps_recvd:
            samps_recvd = min(total_num_samps - total_samps_recvd, samps_recvd)
            result[:, total_samps_recvd:total_samps_recvd + samps_recvd] = \
                recv_buffer[:, 0:samps_recvd]
            total_samps_recvd += samps_recvd
    if skip_samples:
        print("Skipping {} samples.".format(skip_samples))
    return result[0][skip_samples:]

