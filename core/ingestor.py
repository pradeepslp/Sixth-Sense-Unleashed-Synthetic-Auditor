import xmltodict
import json

def parse_scan_data(file_path):
    """
    Parses Nmap XML files to extract vulnerabilities.
    Returns a list of finding objects.
    """
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = xmltodict.parse(f.read())
            
        nmap_run = data.get('nmaprun', {})
        hosts = nmap_run.get('host', [])
        
        if isinstance(hosts, dict): hosts = [hosts]
            
        for host in hosts:
            # 1. Get IP Address
            address = host.get('address', {})
            ip = "Unknown"
            if isinstance(address, list):
                for addr in address:
                    if addr.get('@addrtype') == 'ipv4':
                        ip = addr.get('@addr')
                        break
            elif isinstance(address, dict):
                ip = address.get('@addr', "Unknown")

            # 2. Get Ports & Scripts
            ports_wrapper = host.get('ports', {})
            if not ports_wrapper: continue
            
            ports = ports_wrapper.get('port', [])
            if isinstance(ports, dict): ports = [ports]
            
            for port in ports:
                scripts = port.get('script', [])
                if isinstance(scripts, dict): scripts = [scripts]
                
                for script in scripts:
                    output = script.get('@output', '')
                    title = script.get('@id', 'Unknown Vuln')
                    
                    # --- FIX: ROBUST SEVERITY DETECTION ---
                    # Convert to uppercase to catch "Critical", "CRITICAL", "critical"
                    output_upper = output.upper()
                    
                    severity = "Low" # Default
                    if "CRITICAL" in output_upper: 
                        severity = "Critical"
                    elif "HIGH" in output_upper: 
                        severity = "High"
                    elif "MEDIUM" in output_upper: 
                        severity = "Medium"
                    
                    # Only add if it's a real vulnerability
                    # Accept if it says Vulnerable, Risk Factor, OR explicitly mentions a CVE
                    if "VULNERABLE" in output_upper or "RISK FACTOR" in output_upper or "CVE-" in title.upper():
                        findings.append({
                            'title': title,
                            'severity': severity,
                            'description': output,
                            'host': ip
                        })

    except Exception as e:
        print(f"Error parsing XML: {e}")
        return []
        
    return findings