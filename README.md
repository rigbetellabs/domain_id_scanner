## ROS 2 Domain Scanner

A fast, multi-threaded Python script to scan for active ROS 2 nodes across different domain IDs. It helps you quickly discover which domains are currently in use on your network and what nodes are running on them.

---

## Features

- **Multi-threaded Scanning:** Uses a `ThreadPoolExecutor` to scan multiple domain IDs concurrently, making the process significantly faster.
- **Progress Bar:** Provides a real-time progress bar to visualize the scan's status.
- **Clear Output:** Lists all active domain IDs and the nodes found within each one.
- **Configurable Range:** Easily change the range of domain IDs to scan by modifying the `TOTAL_DOMAINS` variable.
- **Zero Dependencies:** Requires only a standard Python 3 installation and a sourced ROS 2 environment.

---

## Prerequisites

- **Python 3.x**
- **ROS 2** (e.g., Foxy, Humble, Iron) installed and sourced in your terminal.

---

## Usage

1.  **Clone the repository or download the script:**

    ```bash
    git clone https://github.com/rigbetellabs/domain_id_scanner.git
    cd domain_id_scanner
    ```

    or simply save the `ros2_domain_scanner.py` file to your machine.

2.  **Make the script executable (optional but recommended):**

    ```bash
    chmod +x ros2_domain_scanner.py
    ```

3.  **Run the scanner:**
    Make sure you have sourced your ROS 2 environment first\!

    ```bash
    source /opt/ros/humble/setup.bash
    python3 ros2_domain_scanner.py
    ```

---

## Example Output

The script will first display a progress bar while it scans the domains.

```
Scanning: [****************************************] 100%
```

Once complete, it will print a summary of all active domains and their nodes.

```
Scan complete.
Active domain IDs and nodes:

Domain ID 0:
   - /ros2_domain_scanner_node_1
   - /turtlesim

Domain ID 30:
   - /robot_state_publisher
   - /joint_state_publisher
   - /rviz2
```

If no nodes are found on any domain, it will report:

```
No active nodes found in any domain.
```

---

## How It Works

The script iterates through ROS 2 domain IDs from `0` to `232` (as defined by the `TOTAL_DOMAINS` constant). For each domain ID, it performs the following steps in a separate thread:

1.  Sets the `ROS_DOMAIN_ID` environment variable for a subprocess.
2.  Executes the `ros2 node list` command within that environment.
3.  Captures the standard output of the command. If the output is not empty, it means active nodes were found.
4.  A `TimeoutExpired` exception handles cases where a domain is unresponsive, preventing the script from hanging.
5.  All discovered domains and their nodes are collected and displayed at the end of the scan. domain_id_scanner
