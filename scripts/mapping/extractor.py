import re
from collections import defaultdict
import matplotlib.pyplot as plt

class DesignParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.design_info = {}
        self.io_pins = {}
        self.instances = {}
        self.hypergraph = defaultdict(list)
        self._parse_file()

    def _parse_file(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()

        mode = None
        for line in lines:
            line = line.strip()
            if not line or line.startswith('*'):
                continue

            if line.startswith("Basic information of the design"):
                mode = "design"
                continue
            elif line.startswith("Input/Output Pin information"):
                mode = "io"
                continue
            elif line.startswith("Instance information"):
                mode = "inst"
                continue
            elif line.startswith("Nets information"):
                mode = "net"
                continue

            if mode == "design":
                self._parse_design_info(line)
            elif mode == "io":
                self._parse_io_pin(line)
            elif mode == "inst":
                self._parse_instance(line)
            elif mode == "net":
                self._parse_net(line)

    def _parse_design_info(self, line):
        if "Design name" in line:
            self.design_info["design_name"] = line.split(":")[1].strip()
        elif "UNITS DISTANCE" in line:
            self.design_info["units_per_micron"] = int(re.search(r'\d+', line).group())
        elif "Die width" in line:
            self.design_info["die_width"] = int(re.search(r'\d+', line).group())
        elif "Die height" in line:
            self.design_info["die_height"] = int(re.search(r'\d+', line).group())
        elif "Core width" in line:
            self.design_info["core_width"] = int(re.search(r'\d+', line).group())
        elif "Core height" in line:
            self.design_info["core_height"] = int(re.search(r'\d+', line).group())
        elif "Core region" in line:
            coords = list(map(int, re.findall(r'\d+', line)))
            self.design_info["core_region"] = {
                "lx": coords[0], "ly": coords[1], "ux": coords[2], "uy": coords[3]
            }

    def _parse_io_pin(self, line):
        tokens = line.split()
        vid = int(tokens[0])
        self.io_pins[vid] = {
            "name": tokens[1],
            "type": tokens[2],
            "x": int(tokens[3]),
            "y": int(tokens[4])
        }

    def _parse_instance(self, line):
        tokens = line.split()
        vid = int(tokens[0])
        self.instances[vid] = {
            "instance_name": tokens[1],
            "cell_name": tokens[2],
            "is_macro": tokens[3] == "True",
            "is_seq": tokens[4] == "True",
            "is_fixed": tokens[5] == "True",
            "x": int(tokens[6]),
            "y": int(tokens[7]),
            "width": int(tokens[8]),
            "height": int(tokens[9])
        }

    def _parse_net(self, line):
        tokens = list(map(int, line.split()))
        net_id = tokens[0]
        self.hypergraph[net_id].extend(tokens[1:])

    def get_all_vertex_ids(self):
        return list(self.io_pins.keys()) + list(self.instances.keys())

    def get_all_net_ids(self):
        return list(self.hypergraph.keys())

    def summary(self):
        print(f"Design: {self.design_info.get('design_name')}")
        print(f"Die size: {self.design_info.get('die_width')} x {self.design_info.get('die_height')} DBU")
        print(f"Core size: {self.design_info.get('core_width')} x {self.design_info.get('core_height')} DBU")
        print(f"IO Pins: {len(self.io_pins)} | Instances: {len(self.instances)} | Nets: {len(self.hypergraph)}")
    
    #When run, it prints the summary and shows the floorplan:
    #Red = input pins
    #Blue = output pins
    #Gray = standard cells
    #Orange = macros
    #Dashed box = core region
    
    def plot_layout(self):
        if not self.design_info:
            print("Design info missing — cannot plot layout.")
            return

        core = self.design_info["core_region"]
        lx, ly, ux, uy = core["lx"], core["ly"], core["ux"], core["uy"]

        plt.figure(figsize=(10, 10))
        plt.title(f"Layout: {self.design_info.get('design_name')}")
        plt.xlim(0, self.design_info["die_width"])
        plt.ylim(0, self.design_info["die_height"])

        # Draw core region
        plt.gca().add_patch(plt.Rectangle((lx, ly), ux - lx, uy - ly,
                                          edgecolor='black', facecolor='none',
                                          linewidth=1.5, linestyle='--'))

        # Plot I/O pins
        for pin in self.io_pins.values():
            color = 'red' if pin["type"] == "INPUT" else 'blue'
            plt.plot(pin["x"], pin["y"], 'o', color=color, markersize=4)

        # Plot instances
        for inst in self.instances.values():
            if inst["x"] >= 0 and inst["y"] >= 0:
                color = 'orange' if inst["is_macro"] else 'gray'
                x0 = inst["x"] - inst["width"] // 2
                y0 = inst["y"] - inst["height"] // 2
                plt.gca().add_patch(plt.Rectangle((x0, y0), inst["width"], inst["height"],
                                                  facecolor=color, edgecolor='black', linewidth=0.3))

        plt.xlabel("X (DBU)")
        plt.ylabel("Y (DBU)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# -----------------------------
# Main Execution Block
# -----------------------------
if __name__ == "__main__":
    filepath = "ibex_nangate45.txt"
    parser = DesignParser(filepath)
    parser.summary()
    
    # Example: print details for one net and one pin
    sample_net = next(iter(parser.hypergraph))
    sample_pin = next(iter(parser.io_pins))
    print(f"\nSample Net {sample_net}: {parser.hypergraph[sample_net]}")
    print(f"Sample I/O Pin {sample_pin}: {parser.io_pins[sample_pin]}")
    print(parser.hypergraph)
    parser.plot_layout()
