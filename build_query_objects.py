
import argparse
import utility as u
from query import Query
from tqdm import tqdm
from time import time


def main():
    print("Building Query Objects")

    parser = argparse.ArgumentParser(description="Precompute query objects.")
    parser.add_argument("querypath", help="<path/to/queries/>")
    parser.add_argument("-sp", "--savepath", help="<dir/to/save/to/>")
    parser.add_argument("-fo", "--fileorder", default=None,
                        help="Optional path to a .txt file that enforces query processing order.")    
    args = parser.parse_args()

    path = args.querypath
    save_dir = args.savepath
    # Load queries, optionally using .txt file to enforce order
    if args.fileorder is not None:
        with open(args.fileorder, 'r') as f:
            ordered_queries = [line.strip() for line in f if line.strip()]
        available_queries = set(u.get_queries(path))
        stack_queries = [q for q in ordered_queries if q in available_queries]
    else:
        stack_queries = u.get_queries(path)

    save_path = save_dir + "query_objects.pkl"
    save_path_time = save_dir + "query_objects_encoding_time.json"
    query_objects = dict()
    encoding_time = dict()
    for query_name in tqdm(stack_queries):
        t0 = time()
        query_objects[query_name] = Query(query_name, path)
        encoding_time[query_name] = time() - t0

    u.save_pickle(query_objects, save_path)
    u.save_json(encoding_time, save_path_time)
    print("Done")

    return


if __name__ == "__main__":
    main()
