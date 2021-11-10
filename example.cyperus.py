#! /usr/bin/python3

import liblo
from liblo import *
import queue, sys, time
import time

responses = queue.Queue()

class OscServer(ServerThread):
    def __init__(self):
        ServerThread.__init__(self, 5000)
        
    @make_method('/cyperus/address', 'ss')
    def osc_address_handler(self, path, args):
        s = args
        responses.put(s)
        print("received '/cyperus/address'")

    @make_method('/cyperus/list/main', 's')
    def osc_list_main_handler(self, path, args):
        s = args
        responses.put(s)
        print("received '/cyperus/list/main'")

    @make_method('/cyperus/add/bus', 'ssssi')
    def osc_add_bus(self, path, args):
        print("received '/cyperus/add/bus'")

    @make_method('/cyperus/list/bus', 'siis')
    def osc_list_bus(self, path, args):
        print("received '/cyperus/list/bus'")
        responses.put(args)

    @make_method('/cyperus/list/bus_port', 'ss')
    def osc_list_bus_port(self, path, args):
        print("received '/cyperus/list/bus_port'")
        responses.put(args)

    @make_method('/cyperus/add/connection', 'ssi')
    def osc_add_connection(self, path, args):
        print("received '/cyperus/add/connection'")
        print('path', path)
        print('args', args)
        responses.put(args)
        
    @make_method('/cyperus/add/module/audio/oscillator/pulse', 'sffff')
    def osc_add_module_sine(self, path, args):
        print("received '/cyperus/add/module/audio/oscillator/pulse'")
        responses.put(args)

    @make_method('/cyperus/edit/module/audio/oscillator/pulse', 'sffff')
    def osc_edit_module_sine(self, path, args):
        print("received '/cyperus/edit/module/audio/oscillator/pulse'")
        responses.put(args)

    @make_method('/cyperus/add/module/movement/envelope/stdshape', 'siffff')
    def osc_add_module_envelope_stdshape_perc(self, path, args):
        print("received '/cyperus/add/module/movement/envelope/stdshape'")
        responses.put(args)

    @make_method('/cyperus/edit/module/movement/envelope/segment', 'siiiffff')
    def osc_edit_module_envelope_stdshape_perc(self, path, args):
        print("received '/cyperus/edit/module/movement/envelope/segment'")
        responses.put(args)

    @make_method('/cyperus/add/module/audio/filter/moogff', 'sfffff')
    def osc_add_module_moogff(self, path, args):
        print("received '/cyperus/add/module/audio/filter/moogff'")
        responses.put(args)

    @make_method('/cyperus/edit/module/audio/filter/moogff', 'sfffff')
    def osc_edit_module_moogff(self, path, args):
        print("received '/cyperus/edit/module/audio/filter/moogff'")
        responses.put(args)
        
    @make_method('/cyperus/list/module_port', 'ss')
    def osc_list_module_port(self, path, args):
        print("received '/cyperus/list/module_port'")
        responses.put(args)
        
    @make_method(None, None)
    def fallback(self, path, args):
        print("fallback, received '{}'".format(path))
        print("fallback, args '{}'".format(args))
        
def test_single_channel_single_bus_sine_follower_sine(dest):
    mains = {'in': [],
             'out': []}
    bus_main0_uuid = None
    bus_ports  = {'in': [],
                  'out': []}
    sine_module_uuid = None
    sine_module_ports = {'in': [],
                          'out': []}
    envelope_segment_perc_module_uuid = None
    envelope_segment_perc_module_ports = {'in': [],
                          'out': []}
    filter_module_uuid = None
    filter_module_ports = {'in': [],
                          'out': []}
    
    liblo.send(dest, "/cyperus/list/main")
    response = responses.get()
    print('response', response)
    raw_mains = response[0].split('\n')
    outs = False
    for elem in filter(None, raw_mains):
        if elem in 'out:':
            outs = True
        elif elem in 'in:':
            pass
        elif outs:
            mains['out'].append(elem)
        else:
            mains['in'].append(elem)

    liblo.send(dest, "/cyperus/add/bus", "/", "main0", "in", "out")
    liblo.send(dest, "/cyperus/list/bus", "/", 1)
    response = responses.get()
    print('response list bus', response)
    bus_main0_uuid = response[3].split('|')[0]

    print('bus_main0_uuid', bus_main0_uuid)
    
    liblo.send(dest, "/cyperus/list/bus_port", "/{}".format(bus_main0_uuid))
    response = responses.get()

    raw_bus_ports = response[1].split('\n')
    print(raw_bus_ports)
    outs = False
    for elem in filter(None, raw_bus_ports):
        if 'out:' in elem:
            outs = True
        elif 'in:' in elem:
            pass
        elif outs:
            bus_ports['out'].append(elem)
        else:
            bus_ports['in'].append(elem)

    print('bus_ports', bus_ports)
    print('mains', mains)

    print(bus_main0_uuid)
    
    liblo.send(dest, "/cyperus/add/module/audio/oscillator/pulse", "/{}".format(bus_main0_uuid), 440.0, 0.5, 1.0, 0.0)
    response = responses.get()
    sine_module_uuid = response[0]    
    
    liblo.send(dest, "/cyperus/list/module_port", "/{}?{}".format(bus_main0_uuid,
                                                                  sine_module_uuid))
    response = responses.get()
    print('bloc_processor response: {}'.format(response))
    raw_sine_module_ports = response[1].split('\n')
    print(raw_sine_module_ports)
    outs = False
    for elem in filter(None, raw_sine_module_ports):
        if 'out:' in elem:
            outs = True
        elif 'in:' in elem:
            pass
        elif outs:
            sine_module_ports['out'].append(elem)
        else:
            sine_module_ports['in'].append(elem)
    print('sine_module_ports', sine_module_ports)
    
    liblo.send(dest, "/cyperus/add/module/movement/envelope/stdshape",
               "/{}".format(bus_main0_uuid),
               3,     # stdshape (perc=3)
               0.01,  # attack_time
               0.9,   # release_time
               0.5,   # level
               -4.0)  # curve
    response = responses.get()
    envelope_segment_perc_module_uuid = response[0]    
    
    liblo.send(dest, "/cyperus/list/module_port", "/{}?{}".format(bus_main0_uuid,
                                                                  envelope_segment_perc_module_uuid))
    response = responses.get()
    print('bloc_processor response: {}'.format(response))
    raw_envelope_segment_perc_module_ports = response[1].split('\n')
    print(raw_envelope_segment_perc_module_ports)
    outs = False
    for elem in filter(None, raw_envelope_segment_perc_module_ports):
        if 'out:' in elem:
            outs = True
        elif 'in:' in elem:
            pass
        elif outs:
            envelope_segment_perc_module_ports['out'].append(elem)
        else:
            envelope_segment_perc_module_ports['in'].append(elem)
    print('envelope_segment_perc_module_ports', envelope_segment_perc_module_ports)
    
    liblo.send(dest, "/cyperus/add/module/audio/filter/moogff",
               "/{}".format(bus_main0_uuid),
               800.0,
               1.0,
               0.0,
               1.0,
               0.0) # add
    response = responses.get()
    filter_module_uuid = response[0]    
    
    liblo.send(dest, "/cyperus/list/module_port", "/{}?{}".format(bus_main0_uuid,
                                                                  filter_module_uuid))

    response = responses.get()
    print('bloc_processor response: {}'.format(response))
    raw_filter_module_ports = response[1].split('\n')
    print(raw_filter_module_ports)
    outs = False
    for elem in filter(None, raw_filter_module_ports):
        if 'out:' in elem:
            outs = True
        elif 'in:' in elem:
            pass
        elif outs:
            filter_module_ports['out'].append(elem)
        else:
            filter_module_ports['in'].append(elem)
    print('filter_module_ports', filter_module_ports)
    
    
    liblo.send(dest,
               "/cyperus/add/connection",
               "/{}?{}>{}".format(bus_main0_uuid,
                                  envelope_segment_perc_module_uuid,
                                  envelope_segment_perc_module_ports['out'][0].split('|')[0]),
               "/{}?{}<{}".format(bus_main0_uuid,
                                  sine_module_uuid,
                                  sine_module_ports['in'][2].split('|')[0]))
    response = responses.get()    
    
    liblo.send(dest,
               "/cyperus/add/connection",
               "/{}?{}>{}".format(bus_main0_uuid,
                                  sine_module_uuid,
                                  sine_module_ports['out'][0].split('|')[0]),
               "/{}?{}<{}".format(bus_main0_uuid,
                                  filter_module_uuid,
                                  filter_module_ports['in'][0].split('|')[0]))
    response = responses.get()

    liblo.send(dest,
               "/cyperus/add/connection",
               "/{}?{}>{}".format(bus_main0_uuid,
                                  filter_module_uuid,
                                  filter_module_ports['out'][0].split('|')[0]),
               "/{}:{}".format(bus_main0_uuid,
                               bus_ports['out'][0].split('|')[0]))
    response = responses.get()
    
    liblo.send(dest,
               "/cyperus/add/connection",
               "/{}:{}".format(bus_main0_uuid,
                               bus_ports['out'][0].split('|')[0]),
               mains['out'][0])

    response = responses.get()


    time.sleep(5)


    for num in range(0, 800, 5):
        print("/cyperus/edit/module/audio/oscillator/pulse", "/{}?{}".format(bus_main0_uuid, sine_module_uuid), float(num), 0.5, 0.5, 0.0)
        liblo.send(dest, "/cyperus/edit/module/audio/oscillator/pulse", "/{}?{}".format(bus_main0_uuid, sine_module_uuid),  float(num), 0.5, 0.5, 0.0)
        response = responses.get()


        print('sending first edit/module/movement/envelope/segment')
        liblo.send(dest, "/cyperus/edit/module/movement/envelope/segment",
                   "/{}?{}".format(bus_main0_uuid, envelope_segment_perc_module_uuid),
                   -1,  # release_node
                   -1, # loop_node
                   0,  # offset
                   1.0,# gate
                   1.0,# level_scale
                   0.0,# level_bias
                   1.0)# time_scale
        response = responses.get()

        # time.sleep(0.5)

        # print('sending first edit/module/movement/envelope/segment')
        # liblo.send(dest, "/cyperus/edit/module/movement/envelope/segment",
        #            "/{}?{}".format(bus_main0_uuid, envelope_segment_perc_module_uuid),
        #            -1,  # release_node
        #            -1, # loop_node
        #            0,  # offset
        #            -1.0,# gate
        #            1.0,# level_scale
        #            0.0,# level_bias
        #            1.0)# time_scale
        # response = responses.get()

        time.sleep(1.5);

        
if __name__ == '__main__':
    #outgoing connection
    dest = liblo.Address(5001)

    #incoming server
    server = OscServer()

    server.start()

    test_single_channel_single_bus_sine_follower_sine(dest)

    input("press enter to quit...\n")
