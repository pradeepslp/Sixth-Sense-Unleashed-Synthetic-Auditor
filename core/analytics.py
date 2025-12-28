import matplotlib.pyplot as plt
import os

def create_severity_chart(findings, output_path='static/chart.png'):
    """
    Generates a pie chart based on finding severity and saves it to disk.
    """
    # 1. Count Severities
    severity_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
    
    for f in findings:
        sev = f.get('severity', 'Low')
        # Normalize casing (e.g. "high" -> "High")
        sev_key = sev.capitalize() 
        if sev_key in severity_counts:
            severity_counts[sev_key] += 1
        else:
            # Fallback for unexpected labels
            severity_counts['Low'] = severity_counts.get('Low', 0) + 1

    # Filter out zero values so we don't have empty pie slices
    labels = []
    sizes = []
    colors = []
    
    # Define color scheme matching the report severity levels
    color_map = {
        'Critical': '#dc3545', # Red
        'High': '#fd7e14',     # Orange
        'Medium': '#ffc107',   # Yellow
        'Low': '#28a745'       # Green
    }

    for sev, count in severity_counts.items():
        if count > 0:
            labels.append(f"{sev} ({count})")
            sizes.append(count)
            colors.append(color_map.get(sev, '#6c757d'))

    # 2. Generate Plot
    plt.figure(figsize=(6, 4)) # Width, Height in inches
    
    # Create pie chart
    wedges, texts, autotexts = plt.pie(
        sizes, 
        labels=labels, 
        colors=colors, 
        autopct='%1.1f%%', 
        startangle=140,
        textprops=dict(color="black")
    )
    
    plt.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Vulnerability Severity Distribution', pad=20, fontdict={'fontsize': 12, 'fontweight': 'bold'})
    
    # 3. Save to file
    # Ensure static directory exists
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
        
    plt.savefig(output_path, transparent=True, bbox_inches='tight')
    plt.close() # Close figure to free memory
    
    return output_path