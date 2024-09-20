import csv
from math import floor, log
from scipy.stats import pearsonr

from app.repository.datasets import DatasetsRepository


datasets = DatasetsRepository()


def load_data(dataset):
    gw, node = datasets.get(0, dataset)
    dataset_length = min(len(gw), len(node))
    return gw[:dataset_length], node[:dataset_length]


def get_blocks(samples, block_size):
    blocks = []
    num_blocks = floor(len(samples) / block_size)
    for block in range(num_blocks):
        blocks.append(samples[(block * block_size) : ((block + 1) * block_size)])
    return blocks


def remove_zero_indexes(dataset):
    # get measurements and ensure equal length
    gw, node = datasets.get(0, dataset)
    dataset_length = min(len(gw), len(node))
    gw = gw[:dataset_length]
    node = node[:dataset_length]

    before_count = sum([1 for g, n in zip(gw, node) if g == 0 or n == 0])
    gw, node = list(zip(*[(g, n) for g, n in zip(gw, node) if g != 0 and n != 0]))
    after_count = sum([1 for g, n in zip(gw, node) if g == 0 or n == 0])

    print(before_count, after_count)

    with open(dataset + ".cleaned", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["GW RSSI", "NODE RSSI"])
        for g, n in zip(gw, node):
            writer.writerow([g, n])


def preprocess_blocks(samples, function, block_size):
    blocks = get_blocks(samples, block_size)
    return [sample for block in blocks for sample in function(block)]


def preprocess_signal(samples, function):
    return function(samples)


def apply_preprocessing(gw, node, methods, block_size):
    for method in methods:
        gw = preprocess_blocks(gw, method, block_size)
        node = preprocess_blocks(node, method, block_size)
    return gw, node


def split_key(key):
    first = key[: len(key) // 2]
    second = key[len(key) // 2 :]
    return first, second


def get_key_length(keys, key_length):
    new_keys = []
    for key in keys:
        length = len(key)
        if length == key_length * 4:
            first, second = split_key(key)
            f1, f2 = split_key(first)
            s1, s2 = split_key(second)
            new_keys.append(f1)
            new_keys.append(f2)
            new_keys.append(s1)
            new_keys.append(s2)
        elif length == key_length * 2:
            first, second = split_key(key)
            new_keys.append(first)
            new_keys.append(second)
        elif length == key_length:
            new_keys.append(key)
        else:
            raise Exception(f"incompatible key length: {len(key)}")
    return new_keys


def apply_quantisation(gw, node, method, block_size, target_key_length):
    gw_material = "".join([method(block) for block in get_blocks(gw, block_size)])
    node_material = "".join([method(block) for block in get_blocks(node, block_size)])
    print(len(gw_material))
    gw_keys = make_keys(gw_material, target_key_length)
    node_keys = make_keys(node_material, target_key_length)
    print(len(gw_keys[0]))
    return gw_keys, node_keys


def make_keys(key_material, key_length):
    if len(key_material) % key_length != 0:
        raise ValueError("Key length must evenly divide length of key material.")

    splits_needed = int(log(len(key_material) // key_length, 2))
    keys = [key_material]

    for _ in range(splits_needed):
        temp = [split_key(key) for key in keys]
        keys = [x for xs in temp for x in xs]
    return keys


def get_agreed_keys(gw_keys, node_keys):
    return [gwk for gwk, nok in zip(gw_keys, node_keys) if get_bdr(gwk, nok) == 0]


def get_bdr(key_gw, key_node) -> float:
    assert len(key_gw) == len(key_node)
    mismatch = 0
    for i in range(len(key_node)):
        mismatch += 0 if key_node[i] == key_gw[i] else 1
    return mismatch / len(key_node)


def get_correlation(gw, node):
    assert len(gw) == len(node)
    return pearsonr(gw, node).statistic
