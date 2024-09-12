# 这是一个程序去分割一个哈希表（hash map）
#取模分割
# 另一种常见的方法是按键的哈希值对某个固定数字取模，然后根据结果分配键值对。\
# 种方法可以平均分配键值对，降低单个子哈希表的冲突概率。操作步骤包括：
# 1、选择一个合适的模数，通常是一个质数，以减少潜在的模式冲突。
# 2、对每个键的哈希值取模，将键值对分配到对应的子哈希表中。

# 例题如下
# 哈希表中的键值对如下所示：
# hash_map = {
#     10: "apple",
#     23: "banana",
#     37: "cherry",
#     89: "date",
#     45: "elderberry"
# }

# 编写一个函数，该函数接收上述哈希表，并返回三个按取模规则分割的子哈希表的字典。
# 要求使用多线程

import  threading
# 写一个多线程子程序
def thread_func(keys,values,mod_val,thread_index,thread_results):
    # 本地的hash_map 使用｛i:{} for i in range()｝ 内嵌函数快速定义字典
    local_submap = {i:{} for i in range(mod_val)}
    # 使用 zip()打包成一个元组
    for key,value in zip(keys,values):
        index = key % mod_val
        local_submap[index][key] = value
    thread_results[thread_index] = local_submap

# 合并每个线程的sub_map为一个最终的sub_hashmap,能这样写代码的前提是thread_result和final_result 的数据结构是一样的
def merge_map(thread_results, mod_val):
    final_result = { i :{} for i in range(mod_val)}
    for local_submap in thread_results:
        for index in range(mod_val):
            final_result[index].update(local_submap[index])
    return final_result

# 多线程分割子hash_map
def split_map_multithread(hash_map,mod_val,thread_num):
    # 创建一个线程列表和thread_results
    thread_results = [None] * thread_num
    threads=[]

    # 将key和val分配到线程
    keys = list(hash_map.keys())
    values = list(hash_map.values())
    step = len(hash_map) // thread_num + (len(hash_map) % thread_num)

    for i in range(thread_num):
        start = i * step
        end = min(len(hash_map), (start + step))
        thread = threading.Thread(target=thread_func,args=(keys[start:end],values[start:end],mod_val,i,thread_results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return merge_map(thread_results,mod_val)


hash_map = {
    10: "apple",
    23: "banana",
    37: "cherry",
    89: "date",
    45: "elderberry"
}

result = split_map_multithread(hash_map,3,2)
print(result)










