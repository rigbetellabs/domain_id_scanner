import subprocess
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

TOTAL_DOMAINS = 233
progress_count = 0
progress_lock = threading.Lock()


def print_progress_bar(current, total, bar_length=40):
    """Prints a percentage-based progress bar with '*' characters."""
    percent = (current / total) * 100
    filled_len = int(bar_length * (percent / 100))
    bar = "*" * filled_len + "-" * (bar_length - filled_len)
    sys.stdout.write(f"\rScanning: [{bar}] {int(percent)}%")
    sys.stdout.flush()


def check_ros2_nodes(domain_id):
    """Check if there are ROS2 nodes in the given domain."""
    env = os.environ.copy()
    env["ROS_DOMAIN_ID"] = str(domain_id)

    try:
        result = subprocess.run(
            ["ros2", "node", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=env,
            timeout=5,
        )

        output = result.stdout.decode().strip()
        if output:
            nodes = output.splitlines()
            return (domain_id, nodes)
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

    return None


def main():
    global progress_count
    active_domains = {}

    print_progress_bar(0, TOTAL_DOMAINS)

    with ThreadPoolExecutor(max_workers=32) as executor:
        future_to_domain = {
            executor.submit(check_ros2_nodes, i): i for i in range(TOTAL_DOMAINS)
        }

        for future in as_completed(future_to_domain):
            result = future.result()

            with progress_lock:
                progress_count += 1
                print_progress_bar(progress_count, TOTAL_DOMAINS)

            if result is not None:
                domain_id, nodes = result
                active_domains[domain_id] = nodes

    print("\n\nScan complete.")
    if active_domains:
        print("Active domain IDs and nodes:")
        for dom_id in sorted(active_domains):
            print(f"\nDomain ID {dom_id}:")
            for node in active_domains[dom_id]:
                print(f"   - {node}")
    else:
        print("No active nodes found in any domain.")


if __name__ == "__main__":
    main()

