import os, json
from collections import defaultdict
from mylib import files

grid_topo_folder = './grid_topo'
data_folder = './data'

t = input('The IEEE topology bus number: ')
topology = os.path.join(grid_topo_folder, 'grid_topo_' + t + '.json')
# topology = topo_folder + 'topo_' + t + '.json'

def init():
    topo = files.read_file(topology)
    data = []
    data = cal_importance(topo['pmus'], data)
    data = cal_path_num(data)
    return data

def cal_bus_measured(pmus):
    bus_measured = defaultdict(int)
    for pmu in pmus:
        buses = pmu['buses']
        for bus in buses:
            bus_measured[bus] += 1
    return bus_measured

def cal_importance(pmus, data):
    bus_measured = cal_bus_measured(pmus)
    for pmu in pmus:
        pmu_info = {}
        pmu_info['pmu'] = pmu['pmu']
        pmu_info['ip'] = pmu['ip']
        buses = pmu['buses']

        pmu_importance = 0
        for bus in buses:
            pmu_importance += 1/bus_measured[bus]
        pmu_info['pmu_importance'] = pmu_importance
        data.append(pmu_info)
    return data

def cal_path_num(data):
    for d in data:
        pmu_importance = d['pmu_importance']
        if pmu_importance > 4:
            path_num = 3
        elif pmu_importance > 3:
            path_num = 2
        else:
            path_num = 1
        d['path_num'] = path_num
    return data


if __name__ == '__main__':
    data = init()
    files.write_file(os.path.join(data_folder, 'data_' + t + '.json'), json.dumps(data))