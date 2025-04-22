from typing import Dict, Tuple

# Device presets
DEVICE_PRESETS: Dict[str, Dict[str, int]] = {
    "desktop": {"width": 1280, "height": 720},
    "ipad_landscape": {"width": 1024, "height": 768},
    "ipad_portrait": {"width": 768, "height": 1024},
    "iphone_landscape": {"width": 812, "height": 375},
    "iphone_portrait": {"width": 375, "height": 812},
    "small_desktop": {"width": 1024, "height": 768},
    "large_desktop": {"width": 1920, "height": 1080}
}

def get_viewport_size(device: str) -> Tuple[int, int]:
    """Get viewport size for a given device preset."""
    if device not in DEVICE_PRESETS:
        raise ValueError(f"Unknown device preset: {device}. Available presets: {list(DEVICE_PRESETS.keys())}")
    
    preset = DEVICE_PRESETS[device]
    return (preset["width"], preset["height"])

def update_playwright_config(device: str):
    """Update the Playwright configuration file with the specified device viewport."""
    try:
        width, height = get_viewport_size(device)
        
        # Read the current config
        with open("playwright.config.ts", "r") as f:
            config = f.read()
        
        # Update the viewport size
        import re
        config = re.sub(
            r'viewport: { width: \d+, height: \d+ }',
            f'viewport: {{ width: {width}, height: {height} }}',
            config
        )
        
        # Write the updated config
        with open("playwright.config.ts", "w") as f:
            f.write(config)
            
        print(f"Updated Playwright config to {device} resolution: {width}x{height}")
        
    except Exception as e:
        print(f"Error updating Playwright config: {e}")
        raise

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        device = sys.argv[1]
        update_playwright_config(device)
    else:
        print("Available device presets:")
        for device, size in DEVICE_PRESETS.items():
            print(f"  {device}: {size['width']}x{size['height']}") 