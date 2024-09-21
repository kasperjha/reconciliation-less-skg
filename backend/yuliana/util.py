import csv
from math import floor
from scipy.stats import pearsonr
import random

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


def apply_privacy_amplification(gw_keys, node_keys, key_length):
    """
    Privacy amplification implementation using H3 hash method.
    Communicates the random odd number between node and gw in public channel.
    """

    def generate_random_odd_number(bit_length):
        """Generate a random odd number with the specified bit length."""
        number = random.getrandbits(bit_length)
        return number | 1  # Ensure the number is odd by setting the least significant bit

    def h3_hash(input_bits, output_length, a):
        """
        H3 universal hash function.

        :param input_bits: String of '0's and '1's
        :param output_length: Desired length of the output in bits
        :param a: Random odd number used as the hash function parameter
        :return: Hashed output as a string of '0's and '1's
        """
        # Convert input_bits to an integer
        x = int(input_bits, 2)

        # Perform the hash computation
        hashed_value = (a * x) & ((1 << output_length) - 1)

        # Convert the result back to a bit string
        return format(hashed_value, f"0{output_length}b")

    assert len(gw_keys) == len(node_keys)
    random_numbers = [generate_random_odd_number(key_length) for index in range(len(gw_keys))]
    gw_keys = [h3_hash(key, key_length, a) for a, key in zip(random_numbers, gw_keys)]
    node_keys = [h3_hash(key, key_length, a) for a, key in zip(random_numbers, node_keys)]
    return gw_keys, node_keys


def apply_quantisation(gw, node, method, block_size, target_key_length):
    gw_material = "".join([method(block) for block in get_blocks(gw, block_size)])
    node_material = "".join([method(block) for block in get_blocks(node, block_size)])
    gw_keys = make_keys(gw_material, target_key_length)
    node_keys = make_keys(node_material, target_key_length)
    return gw_keys, node_keys


def make_keys(key_material, key_length):
    if len(key_material) % key_length != 0:
        raise ValueError("Key length must evenly divide length of key material.")
    return get_blocks(key_material, key_length)


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
