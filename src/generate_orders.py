#!/usr/bin/env python3
"""
Generate 100 synthetic order records and save them as JSON files
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Target directory
TARGET_DIR = r"data"

def create_directory():
    """Create target directory if it doesn't exist"""
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"Created directory: {TARGET_DIR}")

def random_date(start_date: str, end_date: str) -> str:
    """Generate random date between start_date and end_date"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    random_days = random.randint(0, (end - start).days)
    random_date = start + timedelta(days=random_days)
    
    return random_date.strftime("%Y-%m-%d")

def random_status() -> str:
    """Return random status"""
    statuses = ["Started", "completed", "unexecutable", "pending", "in_progress", ""]
    return random.choice(statuses)

def generate_resource() -> Dict[str, Any]:
    """Generate a random resource"""
    resource_types = ["Paint shop", "Fab shop", "Assembly shop", "Quality Control", "Packaging", "Shipping"]
    resource_names = [
        "Metro Paint Center", "Industrial Coating Co", "Prime Fabrication", "Steel Works LLC",
        "Precision Assembly", "Quality First Labs", "PackRight Solutions", "FastShip Logistics",
        "Advanced Manufacturing", "Custom Metal Works", "TechPak Industries", "Reliable Transport",
        "Elite Finishing", "Apex Manufacturing", "Premier Assembly", "Global Logistics",
        "Precision Paint Works", "Industrial Solutions", "Quick Pack Pro", "Superior Fab"
    ]
    units = ["day", "hour", "piece", "batch"]
    
    return {
        "resource_id": random.randint(1, 1000),
        "resource_name": random.choice(resource_names),
        "resource_type": random.choice(resource_types),
        "resource_quantity": random.randint(1, 25),
        "resource_unit": random.choice(units)
    }

def generate_dependency_order(level: int = 2, order_number: int = None) -> Dict[str, Any]:
    """Generate a dependency order"""
    if order_number is None:
        order_number = random.randint(10000, 99999)
    
    schedule_start = random_date("2024-01-01", "2024-06-01")
    schedule_end = random_date("2024-06-01", "2024-12-31")
    
    order = {
        "order_number": order_number,
        "schecule_start_date": schedule_start,
        "schecule_end_date": schedule_end,
        "actual_start_date": random_date("2024-01-01", "2024-10-01") if random.random() > 0.35 else "",
        "description": f"This is a {'2nd' if level == 2 else '3rd'} level order",
        "status": random_status()
    }
    
    # Add actual_end_date for some completed/started orders
    if (order["status"] in ["completed", "Started"]) and order["actual_start_date"] and random.random() > 0.4:
        order["actual_end_date"] = random_date(order["actual_start_date"], "2024-12-31")
    
    # 2nd level orders might have 3rd level dependencies
    if level == 2 and random.random() > 0.5:
        order["dependencies"] = []
        num_deps = random.randint(1, 4)
        for _ in range(num_deps):
            order["dependencies"].append(generate_dependency_order(3))
    
    return order

def generate_main_order(order_number: int, dependency_pool: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate a main order"""
    num_resources = random.randint(1, 5)
    num_dependencies = random.randint(1, 5)
    
    schedule_start = random_date("2024-01-01", "2024-04-01")
    schedule_end = random_date("2024-08-01", "2024-12-31")
    
    order = {
        "order_number": order_number,
        "schecule_start_date": schedule_start,
        "schecule_end_date": schedule_end,
        "actual_start_date": random_date("2024-01-01", "2024-09-01") if random.random() > 0.3 else "",
        "description": "This is a 1st level order",
        "status": random_status(),
        "dependencies": [],
        "resources": []
    }
    
    # Add dependencies (70% chance to reuse existing, 30% chance to create new)
    for _ in range(num_dependencies):
        if random.random() > 0.3 and dependency_pool:
            # Reuse an existing dependency order (deep copy)
            reused_order = random.choice(dependency_pool)
            order["dependencies"].append(json.loads(json.dumps(reused_order)))
        else:
            # Create a new dependency order
            order["dependencies"].append(generate_dependency_order(2))
    
    # Add resources
    for _ in range(num_resources):
        order["resources"].append(generate_resource())
    
    return order

def generate_all_orders() -> List[Dict[str, Any]]:
    """Generate all 100 orders with shared dependency pool"""
    print("Generating dependency pool...")
    
    # Generate a pool of 50 dependency orders that can be reused
    dependency_pool = []
    for _ in range(50):
        dependency_pool.append(generate_dependency_order(2))
    
    print("Generating 100 main orders...")
    
    # Generate 100 main orders with sequential numbers starting from 80000
    orders = []
    for i in range(100):
        order_number = 80000 + i
        order = generate_main_order(order_number, dependency_pool)
        orders.append(order)
        
        if (i + 1) % 10 == 0:
            print(f"Generated {i + 1} orders...")
    
    return orders

def save_orders(orders: List[Dict[str, Any]]):
    """Save orders to individual JSON files"""
    saved_files = 0
    errors = 0
    
    for order in orders:
        filename = f"{order['order_number']}.json"
        filepath = os.path.join(TARGET_DIR, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(order, f, indent=2, ensure_ascii=False)
            saved_files += 1
            
            if saved_files % 10 == 0:
                print(f"Saved {saved_files} files...")
                
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            errors += 1
    
    return saved_files, errors

def analyze_dependencies(orders: List[Dict[str, Any]]):
    """Analyze dependency patterns"""
    all_dependencies = []
    
    def extract_deps(deps):
        for dep in deps:
            all_dependencies.append(dep["order_number"])
            if "dependencies" in dep and dep["dependencies"]:
                extract_deps(dep["dependencies"])
    
    for order in orders:
        extract_deps(order["dependencies"])
    
    unique_dependencies = list(set(all_dependencies))
    
    # Count dependency usage
    dependency_count = {}
    for dep in all_dependencies:
        dependency_count[dep] = dependency_count.get(dep, 0) + 1
    
    reused_dependencies = [(dep, count) for dep, count in dependency_count.items() if count > 1]
    reused_dependencies.sort(key=lambda x: x[1], reverse=True)
    
    return {
        'total_dependencies': len(all_dependencies),
        'unique_dependencies': len(unique_dependencies),
        'reused_dependencies': len(reused_dependencies),
        'most_reused': reused_dependencies[:5]
    }

def main():
    """Main function"""
    print("🚀 Starting synthetic order generation...")
    print(f"📁 Target directory: {TARGET_DIR}")
    
    # Create directory
    create_directory()
    
    # Generate orders
    orders = generate_all_orders()
    
    # Save orders
    print("\n💾 Saving orders to files...")
    saved_files, errors = save_orders(orders)
    
    # Display results
    print(f"\n✅ Generation complete!")
    print(f"📁 Directory: {TARGET_DIR}")
    print(f"📄 Files saved: {saved_files}")
    print(f"❌ Errors: {errors}")
    
    # Analyze dependencies
    print("\n📊 Analyzing dependencies...")
    stats = analyze_dependencies(orders)
    
    print(f"\n📊 Statistics:")
    print(f"   Total main orders: {len(orders)}")
    print(f"   Total dependency instances: {stats['total_dependencies']}")
    print(f"   Unique dependency orders: {stats['unique_dependencies']}")
    print(f"   Reused dependency orders: {stats['reused_dependencies']}")
    
    if stats['most_reused']:
        print(f"\n🔄 Most reused dependencies:")
        for order_num, count in stats['most_reused']:
            print(f"   Order {order_num}: used {count} times")
    
    print(f"\n🎉 All files have been generated and saved to:")
    print(f"   {TARGET_DIR}")

if __name__ == "__main__":
    main()