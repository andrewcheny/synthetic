import json
import os
from pyvis.network import Network

def load_order_data(data_dir):
    """Load all JSON files from the data directory"""
    orders = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            with open(os.path.join(data_dir, filename), 'r') as f:
                orders.append(json.load(f))
    return orders

def add_order_to_network(net, order, level=0, parent_id=None):
    """Recursively add orders and their dependencies to the network"""
    order_id = str(order['order_number'])
    
    # Generate stars based on dependency level
    stars = "★" * (level + 1) if level > 0 else ""
    
    # Determine node color based on level and status
    if level == 0:  # Top level orders
        color = 'white'
    else:  # Dependency orders
        color = 'green'
    
    # Override color to red if status is "pending"
    if order['status'].lower() == 'pending':
        color = 'red'
    
    # Add the node with stars for dependency level
    label = f"{stars} Order {order['order_number']}" if stars else f"Order {order['order_number']}"
    net.add_node(
        order_id,
        label=label,
        color=color,
        title=f"Order: {order['order_number']}\nLevel: {level}\nStatus: {order['status']}\nDescription: {order['description']}",
        group=f"level_{level}",
        level=level,
        status=order['status'].lower(),
        shape='dot'
    )
    
    # Add edge from parent if exists
    if parent_id:
        net.add_edge(parent_id, order_id)
    
    # Add resources as orange squares
    if 'resources' in order:
        for i, resource in enumerate(order['resources']):
            resource_id = f"res_{order_id}_{i}"
            net.add_node(
                resource_id,
                label=f"R{resource['resource_id']}",
                color='orange',
                title=f"Resource: {resource['resource_name']}\nType: {resource['resource_type']}\nQuantity: {resource['resource_quantity']} {resource['resource_unit']}",
                shape='square',
                group="resource",
                level=-1
            )
            net.add_edge(order_id, resource_id, color='orange', width=2)
    
    # Process dependencies recursively
    if 'dependencies' in order:
        for dependency in order['dependencies']:
            add_order_to_network(net, dependency, level + 1, order_id)

def visualize_orders(data_dir='data', output_file='order_visualization.html', max_orders=20):
    """Create and save the order visualization"""
    # Load order data
    orders = load_order_data(data_dir)
    
    # Limit to first N orders to reduce crowding
    orders = orders[:max_orders]
    
    # Create network with enhanced features
    net = Network(
        height="800px",
        width="100%",
        bgcolor="#222222",
        font_color="white",
        directed=True,
        filter_menu=True,
        select_menu=True,
        neighborhood_highlight=True
    )
    
    # Configure advanced physics and interaction options
    net.set_options("""
    var options = {
      "physics": {
        "enabled": true,
        "solver": "hierarchicalRepulsion",
        "stabilization": {"iterations": 200},
        "hierarchicalRepulsion": {
          "centralGravity": 0.0,
          "springLength": 100,
          "springConstant": 0.01,
          "nodeDistance": 120,
          "damping": 0.09
        }
      },
      "layout": {
        "hierarchical": {
          "enabled": true,
          "levelSeparation": 150,
          "nodeSpacing": 100,
          "treeSpacing": 200,
          "blockShifting": true,
          "edgeMinimization": true,
          "parentCentralization": true,
          "direction": "UD",
          "sortMethod": "directed"
        }
      },
      "interaction": {
        "navigationButtons": true,
        "keyboard": true,
        "hover": true,
        "selectConnectedEdges": false,
        "zoomView": true,
        "dragView": true
      },
      "manipulation": {
        "enabled": false
      }
    }
    """)
    
    # Add all orders to the network
    for order in orders:
        add_order_to_network(net, order)
    
    # First generate the basic HTML with pyvis
    net.save_graph(output_file)
    
    # Read the generated HTML to extract the network data
    with open(output_file, 'r', encoding='utf-8') as f:
        original_html = f.read()
    
    # Extract the nodes and edges data from the original HTML
    import re
    nodes_match = re.search(r'nodes = new vis\.DataSet\((.*?)\);', original_html, re.DOTALL)
    edges_match = re.search(r'edges = new vis\.DataSet\((.*?)\);', original_html, re.DOTALL)
    
    if not nodes_match or not edges_match:
        print("Error: Could not extract network data from generated HTML")
        return output_file
    
    nodes_data = nodes_match.group(1)
    edges_data = edges_match.group(1)
    
    # Create enhanced HTML template
    enhanced_html = f"""<!doctype html>
<html>
<head>
    <title>Order Dependency Visualization</title>
    <meta charset="utf-8">
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 10px; background: #222; color: white; }}
        #controls {{ 
            background: #333; 
            padding: 15px; 
            margin-bottom: 10px; 
            border-radius: 5px;
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            align-items: center;
        }}
        .control-group {{ display: flex; flex-direction: column; gap: 5px; }}
        .control-group label {{ font-size: 12px; color: #ccc; }}
        select, button {{ 
            background: #444; 
            color: white; 
            border: 1px solid #666; 
            padding: 5px 10px; 
            border-radius: 3px;
        }}
        button:hover {{ background: #555; cursor: pointer; }}
        #mynetworkid {{ border: 1px solid #666; height: 600px; }}
        .legend {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0,0,0,0.8);
            padding: 10px;
            border-radius: 5px;
            font-size: 12px;
            z-index: 1000;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }}
        .legend-color {{
            width: 15px;
            height: 15px;
            margin-right: 8px;
            border: 1px solid #666;
        }}
    </style>
</head>
<body>
    <div id="controls">
        <div class="control-group">
            <label>Solver:</label>
            <select id="solver">
                <option value="hierarchicalRepulsion">Hierarchical</option>
                <option value="repulsion">Repulsion</option>
                <option value="barnesHut">Barnes Hut</option>
                <option value="forceAtlas2Based">Force Atlas</option>
            </select>
        </div>
        <div class="control-group">
            <label>Layout:</label>
            <select id="layout">
                <option value="hierarchical">Hierarchical</option>
                <option value="physics">Physics</option>
                <option value="random">Random</option>
            </select>
        </div>
        <div class="control-group">
            <label>Filter Status:</label>
            <select id="statusFilter">
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="started">Started</option>
            </select>
        </div>
        <div class="control-group">
            <label>Filter Level:</label>
            <select id="levelFilter">
                <option value="all">All Levels</option>
                <option value="0">Level 0 (Top)</option>
                <option value="1">Level 1</option>
                <option value="2">Level 2</option>
                <option value="3">Level 3+</option>
            </select>
        </div>
        <button id="resetView">Reset View</button>
        <button id="fitView">Fit All</button>
        <button id="togglePhysics">Toggle Physics</button>
        <button id="exportView">Export PNG</button>
    </div>
    <div class="legend">
        <div class="legend-item">
            <div class="legend-color" style="background: white;"></div>
            <span>Top Level Orders</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: green;"></div>
            <span>Dependencies</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: red;"></div>
            <span>Pending Status</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: orange;"></div>
            <span>Resources</span>
        </div>
        <div style="margin-top: 10px; font-size: 10px; color: #999;">
            ★ = Dependency Level<br>
            □ = Resources<br>
            ○ = Orders
        </div>
    </div>
    <div id="mynetworkid"></div>
    
    <script type="text/javascript">
        // Network data
        var nodes = new vis.DataSet({nodes_data});
        var edges = new vis.DataSet({edges_data});
        
        // Create network
        var container = document.getElementById('mynetworkid');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        var options = {{
            physics: {{
                enabled: true,
                solver: "hierarchicalRepulsion",
                stabilization: {{iterations: 200}},
                hierarchicalRepulsion: {{
                    centralGravity: 0.0,
                    springLength: 100,
                    springConstant: 0.01,
                    nodeDistance: 120,
                    damping: 0.09
                }}
            }},
            layout: {{
                hierarchical: {{
                    enabled: true,
                    levelSeparation: 150,
                    nodeSpacing: 100,
                    treeSpacing: 200,
                    blockShifting: true,
                    edgeMinimization: true,
                    parentCentralization: true,
                    direction: "UD",
                    sortMethod: "directed"
                }}
            }},
            interaction: {{
                navigationButtons: true,
                keyboard: true,
                hover: true,
                selectConnectedEdges: false,
                zoomView: true,
                dragView: true
            }},
            manipulation: {{
                enabled: false
            }}
        }};
        
        var network = new vis.Network(container, data, options);
        
        // Enhanced controls functionality
        let physicsEnabled = true;
        let allNodes = nodes.get();
        let allEdges = edges.get();
        
        // Solver change handler
        document.getElementById('solver').addEventListener('change', function() {{
            let solver = this.value;
            let options = {{
                physics: {{
                    enabled: true,
                    solver: solver,
                    stabilization: {{iterations: 200}}
                }}
            }};
            
            if (solver === 'hierarchicalRepulsion') {{
                options.physics.hierarchicalRepulsion = {{
                    centralGravity: 0.0,
                    springLength: 100,
                    springConstant: 0.01,
                    nodeDistance: 120,
                    damping: 0.09
                }};
            }}
            
            network.setOptions(options);
        }});
        
        // Layout change handler
        document.getElementById('layout').addEventListener('change', function() {{
            let layout = this.value;
            let options = {{}};
            
            if (layout === 'hierarchical') {{
                options.layout = {{
                    hierarchical: {{
                        enabled: true,
                        levelSeparation: 150,
                        nodeSpacing: 100,
                        treeSpacing: 200,
                        direction: 'UD',
                        sortMethod: 'directed'
                    }}
                }};
                options.physics = {{enabled: true}};
            }} else if (layout === 'physics') {{
                options.layout = {{hierarchical: {{enabled: false}}}};
                options.physics = {{enabled: true}};
            }} else {{
                options.layout = {{hierarchical: {{enabled: false}}}};
                options.physics = {{enabled: false}};
                network.setData({{nodes: nodes, edges: edges}});
                network.redraw();
            }}
            
            network.setOptions(options);
        }});
        
        // Status filter
        document.getElementById('statusFilter').addEventListener('change', function() {{
            applyFilters();
        }});
        
        // Level filter
        document.getElementById('levelFilter').addEventListener('change', function() {{
            applyFilters();
        }});
        
        function applyFilters() {{
            let statusFilter = document.getElementById('statusFilter').value;
            let levelFilter = document.getElementById('levelFilter').value;
            
            let filteredNodes = allNodes.filter(node => {{
                let statusMatch = statusFilter === 'all' || node.status === statusFilter;
                let levelMatch = levelFilter === 'all' || 
                    (levelFilter === '3' && node.level >= 3) ||
                    node.level.toString() === levelFilter ||
                    node.group === 'resource';
                
                return statusMatch && levelMatch;
            }});
            
            let filteredNodeIds = new Set(filteredNodes.map(n => n.id));
            let filteredEdges = allEdges.filter(edge => 
                filteredNodeIds.has(edge.from) && filteredNodeIds.has(edge.to)
            );
            
            nodes.clear();
            edges.clear();
            nodes.add(filteredNodes);
            edges.add(filteredEdges);
        }}
        
        // Navigation buttons
        document.getElementById('resetView').addEventListener('click', function() {{
            network.moveTo({{position: {{x: 0, y: 0}}, scale: 1}});
        }});
        
        document.getElementById('fitView').addEventListener('click', function() {{
            network.fit();
        }});
        
        document.getElementById('togglePhysics').addEventListener('click', function() {{
            physicsEnabled = !physicsEnabled;
            network.setOptions({{physics: {{enabled: physicsEnabled}}}});
            this.textContent = physicsEnabled ? 'Toggle Physics' : 'Toggle Physics';
        }});
        
        document.getElementById('exportView').addEventListener('click', function() {{
            let canvas = document.querySelector('#mynetworkid canvas');
            if (canvas) {{
                let link = document.createElement('a');
                link.download = 'order_visualization.png';
                link.href = canvas.toDataURL();
                link.click();
            }}
        }});
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(event) {{
            if (event.key === 'r' || event.key === 'R') {{
                document.getElementById('resetView').click();
            }} else if (event.key === 'f' || event.key === 'F') {{
                document.getElementById('fitView').click();
            }} else if (event.key === 'p' || event.key === 'P') {{
                document.getElementById('togglePhysics').click();
            }}
        }});
        
        // Highlighting on selection
        network.on('select', function(params) {{
            if (params.nodes.length > 0) {{
                let selectedNode = params.nodes[0];
                let connectedNodes = network.getConnectedNodes(selectedNode);
                
                let updateArray = [];
                allNodes.forEach(node => {{
                    if (node.id === selectedNode || connectedNodes.indexOf(node.id) > -1) {{
                        updateArray.push({{id: node.id, opacity: 1}});
                    }} else {{
                        updateArray.push({{id: node.id, opacity: 0.3}});
                    }}
                }});
                
                nodes.update(updateArray);
            }} else {{
                // Reset opacity
                let updateArray = allNodes.map(node => ({{id: node.id, opacity: 1}}));
                nodes.update(updateArray);
            }}
        }});
    </script>
</body>
</html>"""
    
    # Write the enhanced HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(enhanced_html)
    
    print(f"Enhanced visualization saved to {output_file}")
    return output_file

if __name__ == "__main__":
    visualize_orders()