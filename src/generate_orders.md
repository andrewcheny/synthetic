# Synthetic Order Generator - Instructions

## Overview

This Python script generates 100 synthetic order records based on the structure of your original `76451.json` file. The generated data maintains all the key patterns including shared dependencies, hierarchical structures, and realistic data patterns.

## Features

- **100 Main Orders**: Creates orders numbered 80000-80099
- **Shared Dependencies**: Uses a pool of 50 dependency orders that get reused across multiple main orders
- **Hierarchical Structure**: Maintains 1st → 2nd → 3rd level order dependencies
- **Realistic Data Patterns**:
  - Various status values: "Started", "completed", "unexecutable", "pending", "in_progress", ""
  - Mix of filled and empty `actual_start_date` fields
  - `actual_end_date` appears only for some completed/started orders
  - Different resource types and quantities
- **Dependency Reuse**: 70% chance to reuse existing dependencies, 30% chance to create new ones
- **Statistics**: Provides detailed analysis of dependency reuse patterns

## Prerequisites

- Python 3.6 or higher
- No additional libraries required (uses only Python standard library)

## Installation & Setup

1. **Save the Script**
   - Copy the Python code into a file named `generate_orders.py`
   - Save it to any location on your computer

2. **Verify Target Directory**
   - The script will create files in: `C:\Users\HQSACTCHENYanCTR-AI\OneDrive - NATO Public Cloud\Documents\spectrum\synthetic_data`
   - The directory will be created automatically if it doesn't exist

## How to Run

### Method 1: Command Prompt
1. Open **Command Prompt** (Windows + R, type `cmd`, press Enter)
2. Navigate to where you saved the script:
   ```
   cd "path\to\your\script\location"
   ```
3. Run the script:
   ```
   python generate_orders.py
   ```

### Method 2: Python IDLE
1. Open **Python IDLE**
2. Open the script file: File → Open → select `generate_orders.py`
3. Run the script: Run → Run Module (or press F5)

### Method 3: Visual Studio Code / PyCharm
1. Open the script in your IDE
2. Right-click and select "Run Python File"
3. Or use the IDE's run button

## Expected Output

When you run the script, you'll see output like this:

```
🚀 Starting synthetic order generation...
📁 Target directory: C:\Users\HQSACTCHENYanCTR-AI\OneDrive - NATO Public Cloud\Documents\spectrum\synthetic_data
Created directory: [directory path]
Generating dependency pool...
Generating 100 main orders...
Generated 10 orders...
Generated 20 orders...
Generated 30 orders...
...
Generated 100 orders...

💾 Saving orders to files...
Saved 10 files...
Saved 20 files...
...
Saved 100 files...

✅ Generation complete!
📁 Directory: C:\Users\HQSACTCHENYanCTR-AI\OneDrive - NATO Public Cloud\Documents\spectrum\synthetic_data
📄 Files saved: 100
❌ Errors: 0

📊 Analyzing dependencies...

📊 Statistics:
   Total main orders: 100
   Total dependency instances: 347
   Unique dependency orders: 73
   Reused dependency orders: 28

🔄 Most reused dependencies:
   Order 45892: used 8 times
   Order 23451: used 6 times
   Order 67834: used 5 times
   Order 34567: used 5 times
   Order 78234: used 4 times

🎉 All files have been generated and saved to:
   C:\Users\HQSACTCHENYanCTR-AI\OneDrive - NATO Public Cloud\Documents\spectrum\synthetic_data
```

## Generated Files

After successful execution, you'll have:

- **100 JSON files** named `80000.json` through `80099.json`
- Each file follows the exact structure of your original `76451.json`
- Files will be saved in the specified directory

## File Structure

Each generated JSON file contains:

```json
{
    "order_number": 80000,
    "schecule_start_date": "2024-01-15",
    "schecule_end_date": "2024-11-30",
    "actual_start_date": "2024-02-01",
    "description": "This is a 1st level order",
    "status": "Started",
    "dependencies": [
        {
            "order_number": 68233,
            "schecule_start_date": "2024-01-15",
            "schecule_end_date": "2024-08-15",
            "actual_start_date": "2024-01-20",
            "description": "This is 2nd level order",
            "status": "completed",
            "actual_end_date": "2024-07-30",
            "dependencies": [...]
        }
    ],
    "resources": [
        {
            "resource_id": 101,
            "resource_name": "Metro Paint Center",
            "resource_type": "Paint shop",
            "resource_quantity": 8,
            "resource_unit": "day"
        }
    ]
}
```

## Key Data Patterns

1. **Main Orders**: Order numbers 80000-80099 (these are the filenames)
2. **Dependency Orders**: Lower order numbers that appear within the dependencies
3. **Shared Dependencies**: The same dependency order can appear in multiple main orders
4. **No Circular Dependencies**: Dependency orders never appear as top-level main orders
5. **Realistic Dates**: Dates span throughout 2024 with logical sequences
6. **Resource Variety**: Different resource types, names, quantities, and units

## Customization

To modify the generated data, you can edit these variables in the script:

- **Number of orders**: Change the range in the main generation loop
- **Order number range**: Modify the starting number (currently 80000)
- **Date ranges**: Adjust the date parameters in `random_date()` calls
- **Status options**: Modify the `statuses` list in `random_status()`
- **Resource types/names**: Edit the lists in `generate_resource()`
- **Dependency reuse ratio**: Change the probability in the dependency generation logic

## Troubleshooting

### Common Issues:

1. **Permission Error**
   - Make sure you have write permissions to the target directory
   - Try running Command Prompt as Administrator

2. **Python Not Found**
   - Install Python from https://python.org
   - Make sure Python is added to your system PATH

3. **Directory Creation Failed**
   - Check if the OneDrive path exists and is accessible
   - You can modify the `TARGET_DIR` variable in the script to use a different location

4. **Script Doesn't Run**
   - Make sure the file is saved with `.py` extension
   - Check for any copy-paste errors in the code

### Getting Help:

If you encounter issues:
1. Check the error message displayed in the console
2. Verify Python installation: `python --version`
3. Test with a simpler directory path first
4. Make sure the script file is complete and properly formatted

## File Locations

- **Script**: Save as `generate_orders.py` in any location
- **Output**: Files will be created in `C:\Users\HQSACTCHENYanCTR-AI\OneDrive - NATO Public Cloud\Documents\spectrum\synthetic_data\`
- **Naming**: Files named as `{order_number}.json` (e.g., `80000.json`, `80001.json`, etc.)

## Success Indicators

You'll know the script worked correctly when:
- ✅ You see "Generation complete!" message
- ✅ 100 files are created in the target directory
- ✅ Statistics show dependency reuse patterns
- ✅ No error messages appear
- ✅ Each JSON file opens correctly and follows the expected structure