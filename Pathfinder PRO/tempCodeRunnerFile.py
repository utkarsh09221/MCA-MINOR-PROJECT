import tkinter as tk
from tkinter import ttk
import networkx as nx
import random
 
# Node colors
VISITED_COLOR = 'blue'
CURRENT_COLOR = 'green'
PATH_COLOR = 'red'
 
class PathfindingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pathfinding Algorithms")
        self.master.geometry("1200x700")
        
        # Set background color to greyish
        self.master.configure(bg="#D3D3D3")  # Greyish background for the main window
 
        self.G = nx.Graph()  
        self.node_positions = {}
        self.start_node = None
        self.end_node = None
        self.visited_nodes = set()
        self.current_algorithm = tk.StringVar(value="Select Algorithm")
        self.dls_limit = tk.IntVar(value=3)  # Initial DLS limit
 
        # Apply some basic styles to improve appearance
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=10)
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TScale", font=("Arial", 12))
        self.style.configure("Treeview", font=("Arial", 10))
 
        # Create main layout frames
        self.main_frame = ttk.Frame(self.master, style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
 
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20)
 
        # Replace ttk.Frame with tk.Frame for the sidebar frame
        self.sidebar_frame = tk.Frame(self.main_frame, bg="#D3D3D3")  # Set sidebar to greyish
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)
 
 
        # Algorithm selection
        self.algorithm_menu = tk.OptionMenu(self.sidebar_frame, self.current_algorithm, "BFS", "DFS", "DLS")
        self.algorithm_menu.pack(pady=15)
 
        # Depth-Limited Search (DLS) limit input
        self.dls_limit_label = ttk.Label(self.sidebar_frame, text="Set Depth Limit for DLS:")
        self.dls_limit_label.pack(pady=5)
        self.dls_limit_input = ttk.Entry(self.sidebar_frame, textvariable=self.dls_limit, width=5)
        self.dls_limit_input.pack(pady=5)
 
        # Sidebar buttons and instructions
        self.instruction_frame = ttk.Frame(self.sidebar_frame)
        self.instruction_frame.pack(pady=20)
 
        self.instruction_label = ttk.Label(self.instruction_frame, text="Click on nodes to select start and end nodes.", anchor="center")
        self.instruction_label.pack(pady=10)
 
        self.start_button = ttk.Button(self.sidebar_frame, text="Start Algorithm", command=self.start_algorithm)
        self.start_button.pack(pady=10)
 
        self.reset_button = ttk.Button(self.sidebar_frame, text="Reset", command=self.reset)
        self.reset_button.pack(pady=10)
 
        # Button for generating random graph
        self.graph_selection_button = ttk.Button(self.sidebar_frame, text="Generate Random Graph", command=self.generate_random_graph)
        self.graph_selection_button.pack(pady=15)
 
        # Table to display stack/queue
        self.table_frame = ttk.Frame(self.sidebar_frame)
        self.table_frame.pack(pady=10)
        self.treeview = ttk.Treeview(self.table_frame, columns=("Operation", "Node"), show="headings", height=10)
        self.treeview.heading("Operation", text="Operation")
        self.treeview.heading("Node", text="Node")
        self.treeview.pack()
 
        # Canvas for graph visualization
        # Adjusting canvas size
        self.canvas = tk.Canvas(self.canvas_frame, width=1000, height=800, bg="white")  # Larger canvas
        self.canvas.pack()
 
 
        # Control flags
        self.selecting_start = False
        self.selecting_end = False
        self.canvas.bind("<Button-1>", self.select_node)
 
    def generate_random_graph(self):
        """Generate a random graph using NetworkX and update the canvas."""
        self.G.clear()
        self.node_positions.clear()
 
        num_nodes = random.randint(5, 10)
        probability = random.uniform(0.2, 0.6)
        self.G = nx.gnp_random_graph(num_nodes, probability, seed=42)
        self.node_positions = nx.spring_layout(self.G, seed=42)
 
        self.scale_node_positions()
        self.draw_graph()
 
    def scale_node_positions(self):
        """Scale node positions to fit within the canvas size."""
        x_vals = [pos[0] for pos in self.node_positions.values()]
        y_vals = [pos[1] for pos in self.node_positions.values()]
        min_x, max_x = min(x_vals), max(x_vals)
        min_y, max_y = min(y_vals), max(y_vals)
        padding = 50
        canvas_width, canvas_height = 800, 600
 
        for node in self.node_positions:
            x, y = self.node_positions[node]
            scaled_x = padding + (x - min_x) / (max_x - min_x) * (canvas_width - 2 * padding)
            scaled_y = padding + (y - min_y) / (max_y - min_y) * (canvas_height - 2 * padding)
            self.node_positions[node] = (scaled_x, scaled_y)
 
    def select_node(self, event):
        """Select start and end nodes on the canvas."""
        x, y = event.x, event.y
        for node, pos in self.node_positions.items():
            node_x, node_y = int(pos[0]), int(pos[1])
            if abs(node_x - x) < 20 and abs(node_y - y) < 20:
                if not self.selecting_start and not self.selecting_end:
                    self.selecting_start = True
                    self.start_node = node
                    self.instruction_label.config(text="Select the end node.")
                    self.canvas.create_oval(node_x-12, node_y-12, node_x+12, node_y+12, fill="green", outline="black", tags="start_end")
                    return
                elif self.selecting_start and not self.selecting_end:
                    self.selecting_end = True
                    self.end_node = node
                    self.instruction_label.config(text="Starting algorithm...")
                    self.canvas.create_oval(node_x-12, node_y-12, node_x+12, node_y+12, fill="red", outline="black", tags="start_end")
                    return
                elif self.selecting_end:
                    self.selecting_start = True
                    self.start_node = node
                    self.end_node = None
                    self.selecting_end = False
                    self.instruction_label.config(text="Select the end node.")
                    self.canvas.create_oval(node_x-12, node_y-12, node_x+12, node_y+12, fill="green", outline="black", tags="start_end")
                    return
                break
 
    def draw_graph(self):
        """Draw the graph on the canvas."""
        self.canvas.delete("all")
        for node, pos in self.node_positions.items():
            x, y = int(pos[0]), int(pos[1])
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="gray", tags=f"node{node}")
            # Added position offset for better display of node labels
            self.canvas.create_text(x, y-15, text=str(node), font=("Arial", 14, "bold"), tags=f"node{node}")  # Bold numbers
        
        for edge in self.G.edges():
            node1, node2 = edge
            x1, y1 = self.node_positions[node1]
            x2, y2 = self.node_positions[node2]
            self.canvas.create_line(x1, y1, x2, y2)
 
    def start_algorithm(self):
        """Start the selected algorithm."""
        if self.start_node is None or self.end_node is None:
            self.instruction_label.config(text="Please select start and end nodes.")
            return
 
        self.visited_nodes.clear()
        for row in self.treeview.get_children():
            self.treeview.delete(row)
 
        if self.current_algorithm.get() == "BFS":
            self.bfs()
        elif self.current_algorithm.get() == "DFS":
            self.dfs()
        elif self.current_algorithm.get() == "DLS":
            self.dls(self.dls_limit.get())
 
    def bfs(self):
        """Breadth-First Search."""
        queue = [self.start_node]
        parent_map = {self.start_node: None}
        self.visited_nodes.add(self.start_node)
 
        def step_bfs():
            if not queue:
                return
 
            current_node = queue.pop(0)
            self.update_canvas(current_node, visited=True)
            self.update_table("Dequeue", current_node)
 
            if current_node == self.end_node:
                self.reconstruct_path(parent_map)
                return
 
            for neighbor in self.G.neighbors(current_node):
                if neighbor not in self.visited_nodes:
                    queue.append(neighbor)
                    parent_map[neighbor] = current_node
                    self.visited_nodes.add(neighbor)
                    self.update_table("Enqueue", neighbor)
 
            self.master.after(300, step_bfs)
 
        step_bfs()
 
    def dfs(self):
        """Depth-First Search."""
        stack = [self.start_node]
        parent_map = {self.start_node: None}
        self.visited_nodes.add(self.start_node)
 
        def step_dfs():
            if not stack:
                return
 
            current_node = stack.pop()
            self.update_canvas(current_node, visited=True)
            self.update_table("Pop", current_node)
 
            if current_node == self.end_node:
                self.reconstruct_path(parent_map)
                return
 
            for neighbor in self.G.neighbors(current_node):
                if neighbor not in self.visited_nodes:
                    stack.append(neighbor)
                    parent_map[neighbor] = current_node
                    self.visited_nodes.add(neighbor)
                    self.update_table("Push", neighbor)
 
            self.master.after(300, step_dfs)
 
        step_dfs()
 
    def dls(self, depth_limit):
        """Depth-Limited Search."""
        stack = [(self.start_node, 0)]  # (node, depth)
        parent_map = {self.start_node: None}
        self.visited_nodes.add(self.start_node)
 
        def step_dls():
            if not stack:
                return
 
            current_node, current_depth = stack.pop()
            self.update_canvas(current_node, visited=True)
            self.update_table("Pop", current_node)
 
            if current_node == self.end_node:
                self.reconstruct_path(parent_map)
                return
 
            if current_depth < depth_limit:
                for neighbor in self.G.neighbors(current_node):
                    if neighbor not in self.visited_nodes:
                        stack.append((neighbor, current_depth + 1))
                        parent_map[neighbor] = current_node
                        self.visited_nodes.add(neighbor)
                        self.update_table("Push", neighbor)
 
            self.master.after(300, step_dls)
 
        step_dls()
 
def reconstruct_path(self, parent_map):
    """Reconstruct the path from start to end node and highlight it with red lines."""
    path = []
    current_node = self.end_node
    while current_node is not None:
        path.append(current_node)
        current_node = parent_map.get(current_node)

    path.reverse()
    for i in range(len(path) - 1):
        node1 = path[i]
        node2 = path[i + 1]
        x1, y1 = self.node_positions[node1]
        x2, y2 = self.node_positions[node2]
        self.canvas.create_line(x1, y1, x2, y2, fill=PATH_COLOR, width=3)  # Draw red line for path
    for node in path:
        self.update_canvas(node, path=True)

    self.instruction_label.config(text="Algorithm Complete.")

 
    def update_canvas(self, node, visited=False, path=False):
        """Update canvas to show visited nodes and path."""
        x, y = self.node_positions[node]
        if visited:
            self.canvas.create_oval(x-12, y-12, x+12, y+12, fill=VISITED_COLOR, outline="black")
        if path:
            self.canvas.create_oval(x-12, y-12, x+12, y+12, fill=PATH_COLOR, outline="black")
 
    def update_table(self, operation, node):
        """Update the table for stack/queue operations."""
        self.treeview.insert("", "end", values=(operation, node))
 
    def reset(self):
        """Reset the application to its initial state."""
        self.canvas.delete("all")
        self.visited_nodes.clear()
        self.start_node = None
        self.end_node = None
        self.selecting_start = False
        self.selecting_end = False
        self.instruction_label.config(text="Click on nodes to select start and end nodes.")
        self.treeview.delete(*self.treeview.get_children())
if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()