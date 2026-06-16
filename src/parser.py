import pandas as pd
import re
import io

class LogParser:
    def __init__(self):
        # Flexible regex for various custom formats
        self.patterns = [
            # Pattern 1: Nginx/Apache Combined Log format with latency at the end (sometimes added)
            # 127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET / HTTP/1.1" 200 1024 45
            re.compile(r'^(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>.*?)\] "(?P<message>.*?)" (?P<status>\d{3}) (?P<bytes>\d+)(?: (?P<latency>\d+))?'),
            
            # Pattern 2: Typical application log
            # 2023-10-27 10:00:00 [INFO] User login successful - 200 45ms
            re.compile(r'^(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+\[(?P<level>\S+)\]\s+(?P<message>.*?)(?:\s+-\s+(?P<status>\d{3}))?(?:\s+(?P<latency>\d+)(?:ms)?)?$'),
            
            # Pattern 3: Generic fallback
            # Extract anything that ends with HTTP status and latency
            re.compile(r'^(?P<message>.*?)\s+(?P<status>[1-5]\d{2})\s+(?P<latency>\d+)(?:ms)?$')
        ]

    def parse(self, uploaded_file) -> pd.DataFrame:
        filename = uploaded_file.name.lower()
        content = uploaded_file.getvalue().decode('utf-8')
        
        if filename.endswith('.csv'):
            try:
                df = pd.read_csv(io.StringIO(content))
                # standardize column names if possible
                df.columns = [c.lower().strip() for c in df.columns]
                return df
            except Exception as e:
                pass # fallback to text parsing if CSV fails
                
        parsed_data = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            match_found = False
            for pattern in self.patterns:
                match = pattern.match(line)
                if match:
                    data = match.groupdict()
                    parsed_data.append(data)
                    match_found = True
                    break
            
            if not match_found:
                # Absolute fallback: just treat the whole line as message, null for others
                parsed_data.append({'message': line, 'status': None, 'latency': None})
                
        df = pd.DataFrame(parsed_data)
        
        # Ensure numerical columns are correctly typed
        if 'latency' in df.columns:
            df['latency'] = pd.to_numeric(df['latency'], errors='coerce')
        if 'status' in df.columns:
            df['status'] = pd.to_numeric(df['status'], errors='coerce')
            
        return df
