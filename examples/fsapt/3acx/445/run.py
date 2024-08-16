import json
import httpx
import os

from promethium_sdk.utils import (
    base64encode,
    wait_for_workflows_to_complete,
)

foldername = "output"
base_url = os.getenv("PM_API_BASE_URL", "https://api.promethium.qcware.com")
gpu_type = os.getenv("PM_GPU_TYPE", "a100")
workflow_timeout = int(os.getenv("PM_WORKFLOW_TIMEOUT", 864000))
task_timeout = int(os.getenv("PM_TASK_TIMEOUT", 864000))

if not os.path.exists(foldername):
    os.makedirs(foldername)

monomerA = base64encode(
"""
C                    55.520000000000     8.935000000000    30.847000000000
H                    56.439000000000     8.682000000000    30.314000000000
H                    54.997000000000     9.727000000000    30.312000000000
H                    54.882000000000     8.050000000000    30.875000000000
C                    55.895000000000     9.381000000000    32.275000000000
O                    55.196000000000     9.045000000000    33.234000000000
N                    56.985000000000    10.162000000000    32.385000000000
H                    57.536000000000    10.371000000000    31.561000000000
C                    57.403000000000    10.823000000000    33.629000000000
H                    57.399000000000    10.050000000000    34.399000000000
C                    58.821000000000    11.388000000000    33.601000000000
H                    58.926000000000    12.165000000000    32.843000000000
H                    59.096000000000    11.824000000000    34.562000000000
H                    59.548000000000    10.607000000000    33.381000000000
C                    56.429000000000    11.911000000000    34.117000000000
O                    56.448000000000    12.210000000000    35.307000000000
N                    55.576000000000    12.458000000000    33.232000000000
H                    55.596000000000    12.158000000000    32.268000000000
C                    54.519000000000    13.409000000000    33.594000000000
H                    54.986000000000    14.234000000000    34.138000000000
C                    53.893000000000    13.978000000000    32.324000000000
H                    53.433000000000    13.197000000000    31.716000000000
H                    53.117000000000    14.707000000000    32.563000000000
H                    54.637000000000    14.487000000000    31.711000000000
C                    53.443000000000    12.801000000000    34.515000000000
O                    52.944000000000    13.501000000000    35.394000000000
N                    53.150000000000    11.502000000000    34.327000000000
H                    53.601000000000    11.004000000000    33.572000000000
C                    52.278000000000    10.697000000000    35.186000000000
H                    51.368000000000    11.264000000000    35.396000000000
C                    51.897000000000     9.422000000000    34.439000000000
H                    51.285000000000     9.651000000000    33.566000000000
H                    52.771000000000     8.878000000000    34.091000000000
H                    51.316000000000     8.749000000000    35.071000000000
C                    52.937000000000    10.339000000000    36.530000000000
O                    52.234000000000    10.302000000000    37.539000000000
N                    54.266000000000    10.113000000000    36.529000000000
H                    54.768000000000    10.154000000000    35.653000000000
C                    55.080000000000     9.903000000000    37.730000000000
H                    54.596000000000     9.116000000000    38.312000000000
C                    56.462000000000     9.391000000000    37.331000000000
H                    56.391000000000     8.515000000000    36.686000000000
H                    57.043000000000    10.150000000000    36.811000000000
H                    57.032000000000     9.100000000000    38.214000000000
C                    55.137000000000    11.157000000000    38.619000000000
O                    54.984000000000    11.029000000000    39.831000000000
N                    55.328000000000    12.337000000000    38.007000000000
H                    55.483000000000    12.361000000000    37.006000000000
C                    55.372000000000    13.626000000000    38.701000000000
H                    55.971000000000    13.499000000000    39.604000000000
C                    56.080000000000    14.661000000000    37.831000000000
H                    55.550000000000    14.821000000000    36.891000000000
H                    56.148000000000    15.622000000000    38.341000000000
H                    57.096000000000    14.345000000000    37.591000000000
C                    53.979000000000    14.112000000000    39.145000000000
O                    53.894000000000    14.834000000000    40.138000000000
N                    52.916000000000    13.670000000000    38.447000000000
H                    53.073000000000    13.106000000000    37.623000000000
C                    51.521000000000    13.899000000000    38.826000000000
H                    50.877000000000    13.675000000000    37.975000000000
H                    51.362000000000    14.948000000000    39.082000000000
C                    51.116000000000    13.002000000000    40.009000000000
O                    50.323000000000    13.429000000000    40.847000000000
N                    51.696000000000    11.790000000000    40.103000000000
H                    52.309000000000    11.480000000000    39.361000000000
C                    51.606000000000    10.904000000000    41.264000000000
H                    50.555000000000    10.854000000000    41.558000000000
C                    52.032000000000     9.491000000000    40.878000000000
H                    53.073000000000     9.448000000000    40.562000000000
H                    51.919000000000     8.808000000000    41.721000000000
H                    51.420000000000     9.104000000000    40.062000000000
C                    52.387000000000    11.452000000000    42.472000000000
O                    51.854000000000    11.414000000000    43.579000000000
N                    53.614000000000    11.958000000000    42.235000000000
H                    53.990000000000    11.921000000000    41.297000000000
C                    54.485000000000    12.554000000000    43.254000000000
H                    54.576000000000    11.822000000000    44.060000000000
C                    55.891000000000    12.850000000000    42.742000000000
H                    55.891000000000    13.652000000000    42.004000000000
H                    56.550000000000    13.151000000000    43.557000000000
H                    56.335000000000    11.969000000000    42.279000000000
C                    53.879000000000    13.828000000000    43.862000000000
O                    54.041000000000    14.041000000000    45.063000000000
N                    53.150000000000    14.613000000000    43.047000000000
H                    53.106000000000    14.407000000000    42.058000000000
C                    52.272000000000    15.675000000000    43.528000000000
H                    52.878000000000    16.330000000000    44.152000000000
C                    51.729000000000    16.524000000000    42.382000000000
H                    51.136000000000    15.932000000000    41.684000000000
H                    51.092000000000    17.327000000000    42.756000000000
H                    52.540000000000    16.986000000000    41.819000000000
C                    51.140000000000    15.106000000000    44.400000000000
O                    50.958000000000    15.575000000000    45.519000000000
N                    50.414000000000    14.115000000000    43.861000000000
H                    50.657000000000    13.793000000000    42.933000000000
C                    49.221000000000    13.515000000000    44.447000000000
H                    48.902000000000    12.683000000000    43.819000000000
H                    48.412000000000    14.247000000000    44.434000000000
C                    49.425000000000    12.998000000000    45.879000000000
O                    48.585000000000    13.280000000000    46.728000000000
N                    50.533000000000    12.290000000000    46.158000000000
H                    51.197000000000    12.088000000000    45.421000000000
C                    50.790000000000    11.669000000000    47.463000000000
H                    49.848000000000    11.566000000000    48.006000000000
C                    51.352000000000    10.258000000000    47.316000000000
H                    52.320000000000    10.265000000000    46.812000000000
H                    51.485000000000     9.770000000000    48.283000000000
H                    50.680000000000     9.631000000000    46.731000000000
C                    51.729000000000    12.473000000000    48.391000000000
O                    51.874000000000    12.069000000000    49.546000000000
N                    52.360000000000    13.562000000000    47.907000000000
H                    52.196000000000    13.867000000000    46.958000000000
C                    53.383000000000    14.277000000000    48.680000000000
H                    53.142000000000    14.193000000000    49.742000000000
C                    54.742000000000    13.616000000000    48.474000000000
H                    55.043000000000    13.642000000000    47.427000000000
H                    55.512000000000    14.128000000000    49.050000000000
H                    54.733000000000    12.576000000000    48.799000000000
C                    53.452000000000    15.786000000000    48.419000000000
O                    53.633000000000    16.531000000000    49.380000000000
N                    53.289000000000    16.245000000000    47.167000000000
H                    53.159000000000    15.594000000000    46.404000000000
C                    53.239000000000    17.679000000000    46.848000000000
H                    53.210000000000    17.832000000000    45.771000000000
H                    54.151000000000    18.155000000000    47.210000000000
C                    52.011000000000    18.353000000000    47.490000000000
O                    52.120000000000    19.477000000000    47.973000000000
N                    50.886000000000    17.622000000000    47.563000000000
H                    50.882000000000    16.713000000000    47.118000000000
C                    49.674000000000    17.919000000000    48.329000000000
H                    49.258000000000    18.861000000000    47.965000000000
C                    48.649000000000    16.804000000000    48.147000000000
H                    48.372000000000    16.699000000000    47.098000000000
H                    49.030000000000    15.837000000000    48.480000000000
H                    47.733000000000    17.009000000000    48.703000000000
C                    49.923000000000    18.038000000000    49.847000000000
O                    49.357000000000    18.939000000000    50.462000000000
N                    50.768000000000    17.165000000000    50.425000000000
H                    51.195000000000    16.443000000000    49.862000000000
C                    51.125000000000    17.185000000000    51.848000000000
H                    50.199000000000    17.199000000000    52.426000000000
C                    51.922000000000    15.949000000000    52.257000000000
H                    52.893000000000    15.906000000000    51.766000000000
H                    52.106000000000    15.942000000000    53.332000000000
H                    51.384000000000    15.033000000000    52.014000000000
C                    51.929000000000    18.454000000000    52.210000000000
O                    51.729000000000    19.001000000000    53.293000000000
N                    52.756000000000    18.933000000000    51.263000000000
H                    52.854000000000    18.417000000000    50.399000000000
C                    53.495000000000    20.187000000000    51.364000000000
H                    54.206000000000    20.237000000000    50.541000000000
H                    54.064000000000    20.200000000000    52.294000000000
C                    52.573000000000    21.415000000000    51.296000000000
O                    52.829000000000    22.386000000000    52.007000000000
N                    51.497000000000    21.374000000000    50.486000000000
H                    51.335000000000    20.559000000000    49.911000000000
C                    50.492000000000    22.441000000000    50.399000000000
H                    51.026000000000    23.376000000000    50.214000000000
C                    49.547000000000    22.207000000000    49.224000000000
H                    50.099000000000    22.117000000000    48.288000000000
H                    48.955000000000    21.301000000000    49.351000000000
H                    48.850000000000    23.039000000000    49.111000000000
C                    49.682000000000    22.621000000000    51.694000000000
O                    49.402000000000    23.760000000000    52.060000000000
N                    49.351000000000    21.516000000000    52.385000000000
H                    49.598000000000    20.603000000000    52.026000000000
C                    48.671000000000    21.557000000000    53.684000000000
H                    47.823000000000    22.241000000000    53.598000000000
C                    48.120000000000    20.192000000000    54.090000000000
H                    47.602000000000    20.245000000000    55.048000000000
H                    47.407000000000    19.823000000000    53.353000000000
H                    48.916000000000    19.452000000000    54.183000000000
C                    49.596000000000    22.100000000000    54.803000000000
O                    49.116000000000    22.807000000000    55.689000000000
N                    50.903000000000    21.802000000000    54.711000000000
H                    51.219000000000    21.214000000000    53.952000000000
C                    51.944000000000    22.268000000000    55.631000000000
H                    51.555000000000    22.215000000000    56.650000000000
C                    53.139000000000    21.324000000000    55.530000000000
H                    53.585000000000    21.344000000000    54.534000000000
H                    53.918000000000    21.594000000000    56.243000000000
H                    52.849000000000    20.294000000000    55.743000000000
C                    52.409000000000    23.719000000000    55.391000000000
O                    53.117000000000    24.241000000000    56.251000000000
N                    52.051000000000    24.344000000000    54.253000000000
H                    51.460000000000    23.865000000000    53.588000000000
C                    52.575000000000    25.654000000000    53.839000000000
H                    53.662000000000    25.547000000000    53.818000000000
H                    52.301000000000    26.432000000000    54.552000000000
H                    52.216000000000    25.920000000000    52.845000000000
C                    58.425000000000    25.417000000000    46.737000000000
H                    59.127000000000    25.063000000000    45.980000000000
H                    58.906000000000    26.207000000000    47.314000000000
H                    57.548000000000    25.824000000000    46.234000000000
C                    58.065000000000    24.222000000000    47.647000000000
O                    58.867000000000    23.297000000000    47.759000000000
N                    56.856000000000    24.232000000000    48.235000000000
H                    56.243000000000    25.025000000000    48.106000000000
C                    56.344000000000    23.138000000000    49.057000000000
H                    57.158000000000    22.808000000000    49.705000000000
C                    55.221000000000    23.662000000000    49.948000000000
H                    54.336000000000    23.939000000000    49.374000000000
H                    54.931000000000    22.897000000000    50.664000000000
H                    55.538000000000    24.531000000000    50.524000000000
C                    55.891000000000    21.911000000000    48.246000000000
O                    56.118000000000    20.792000000000    48.709000000000
N                    55.316000000000    22.126000000000    47.044000000000
H                    55.125000000000    23.074000000000    46.745000000000
C                    55.057000000000    21.069000000000    46.059000000000
H                    54.467000000000    20.298000000000    46.551000000000
C                    54.264000000000    21.584000000000    44.861000000000
H                    54.065000000000    20.784000000000    44.146000000000
H                    53.299000000000    21.982000000000    45.178000000000
H                    54.789000000000    22.379000000000    44.331000000000
C                    56.365000000000    20.443000000000    45.555000000000
O                    56.469000000000    19.220000000000    45.548000000000
N                    57.333000000000    21.299000000000    45.178000000000
H                    57.142000000000    22.292000000000    45.210000000000
C                    58.662000000000    20.931000000000    44.687000000000
H                    58.517000000000    20.318000000000    43.795000000000
C                    59.400000000000    22.202000000000    44.274000000000
H                    58.848000000000    22.753000000000    43.512000000000
H                    59.560000000000    22.866000000000    45.122000000000
H                    60.379000000000    21.963000000000    43.857000000000
C                    59.464000000000    20.091000000000    45.697000000000
O                    60.132000000000    19.145000000000    45.280000000000
N                    59.349000000000    20.421000000000    46.997000000000
H                    58.802000000000    21.229000000000    47.264000000000
C                    59.959000000000    19.656000000000    48.082000000000
H                    60.986000000000    19.430000000000    47.787000000000
C                    60.040000000000    20.485000000000    49.360000000000
H                    60.626000000000    21.391000000000    49.206000000000
H                    59.049000000000    20.783000000000    49.707000000000
H                    60.513000000000    19.921000000000    50.165000000000
C                    59.253000000000    18.315000000000    48.320000000000
O                    59.947000000000    17.325000000000    48.518000000000
N                    57.912000000000    18.275000000000    48.259000000000
H                    57.391000000000    19.124000000000    48.082000000000
C                    57.147000000000    17.037000000000    48.424000000000
H                    56.086000000000    17.272000000000    48.470000000000
H                    57.425000000000    16.563000000000    49.365000000000
C                    57.408000000000    16.047000000000    47.280000000000
O                    57.513000000000    14.847000000000    47.524000000000
N                    57.578000000000    16.560000000000    46.053000000000
H                    57.455000000000    17.556000000000    45.915000000000
C                    57.949000000000    15.802000000000    44.862000000000
H                    57.313000000000    14.916000000000    44.835000000000
C                    57.617000000000    16.643000000000    43.632000000000
H                    57.849000000000    16.099000000000    42.716000000000
H                    56.557000000000    16.897000000000    43.601000000000
H                    58.187000000000    17.573000000000    43.618000000000
C                    59.409000000000    15.309000000000    44.886000000000
O                    59.662000000000    14.214000000000    44.386000000000
N                    60.319000000000    16.070000000000    45.526000000000
H                    60.039000000000    16.972000000000    45.887000000000
C                    61.694000000000    15.655000000000    45.827000000000
H                    62.151000000000    15.323000000000    44.893000000000
C                    62.494000000000    16.845000000000    46.348000000000
H                    62.457000000000    17.683000000000    45.652000000000
H                    62.143000000000    17.198000000000    47.316000000000
H                    63.544000000000    16.575000000000    46.470000000000
C                    61.730000000000    14.475000000000    46.818000000000
O                    62.380000000000    13.472000000000    46.528000000000
N                    61.009000000000    14.615000000000    47.947000000000
H                    60.502000000000    15.479000000000    48.098000000000
C                    60.886000000000    13.618000000000    49.015000000000
H                    61.893000000000    13.396000000000    49.374000000000
C                    60.079000000000    14.194000000000    50.175000000000
H                    60.547000000000    15.095000000000    50.572000000000
H                    59.065000000000    14.455000000000    49.869000000000
H                    60.002000000000    13.479000000000    50.995000000000
C                    60.258000000000    12.295000000000    48.543000000000
O                    60.676000000000    11.242000000000    49.021000000000
N                    59.290000000000    12.363000000000    47.611000000000
H                    58.982000000000    13.265000000000    47.271000000000
C                    58.608000000000    11.190000000000    47.067000000000
H                    58.474000000000    10.467000000000    47.875000000000
C                    57.211000000000    11.578000000000    46.592000000000
H                    57.240000000000    12.399000000000    45.875000000000
H                    56.706000000000    10.737000000000    46.114000000000
H                    56.598000000000    11.885000000000    47.435000000000
C                    59.413000000000    10.475000000000    45.972000000000
O                    59.317000000000     9.252000000000    45.883000000000
N                    60.237000000000    11.208000000000    45.201000000000
H                    60.264000000000    12.215000000000    45.291000000000
C                    61.235000000000    10.596000000000    44.319000000000
H                    60.721000000000     9.867000000000    43.689000000000
C                    61.862000000000    11.637000000000    43.396000000000
H                    62.586000000000    11.178000000000    42.722000000000
H                    61.104000000000    12.123000000000    42.781000000000
H                    62.381000000000    12.413000000000    43.959000000000
C                    62.309000000000     9.838000000000    45.119000000000
O                    62.741000000000     8.785000000000    44.661000000000
N                    62.669000000000    10.335000000000    46.316000000000
H                    62.275000000000    11.211000000000    46.632000000000
C                    63.590000000000     9.666000000000    47.235000000000
H                    64.452000000000     9.343000000000    46.646000000000
C                    64.121000000000    10.619000000000    48.302000000000
H                    64.615000000000    11.479000000000    47.849000000000
H                    63.323000000000    10.993000000000    48.943000000000
H                    64.852000000000    10.123000000000    48.942000000000
C                    62.991000000000     8.392000000000    47.884000000000
O                    63.742000000000     7.431000000000    48.046000000000
N                    61.670000000000     8.364000000000    48.179000000000
H                    61.114000000000     9.197000000000    48.045000000000
C                    60.935000000000     7.144000000000    48.578000000000
H                    61.389000000000     6.757000000000    49.492000000000
C                    59.458000000000     7.429000000000    48.838000000000
H                    58.931000000000     7.776000000000    47.950000000000
H                    58.945000000000     6.533000000000    49.190000000000
H                    59.340000000000     8.190000000000    49.609000000000
C                    61.022000000000     6.066000000000    47.490000000000
O                    61.383000000000     4.933000000000    47.796000000000
N                    60.693000000000     6.462000000000    46.250000000000
H                    60.398000000000     7.418000000000    46.108000000000
C                    60.684000000000     5.622000000000    45.055000000000
H                    59.997000000000     4.796000000000    45.249000000000
C                    60.144000000000     6.413000000000    43.867000000000
H                    60.084000000000     5.787000000000    42.977000000000
H                    59.142000000000     6.791000000000    44.068000000000
H                    60.779000000000     7.265000000000    43.626000000000
C                    62.064000000000     5.010000000000    44.740000000000
O                    62.128000000000     3.820000000000    44.447000000000
N                    63.130000000000     5.821000000000    44.855000000000
H                    62.981000000000     6.793000000000    45.094000000000
C                    64.523000000000     5.425000000000    44.641000000000
H                    64.573000000000     4.861000000000    43.707000000000
C                    65.369000000000     6.685000000000    44.483000000000
H                    65.021000000000     7.293000000000    43.648000000000
H                    65.339000000000     7.303000000000    45.381000000000
H                    66.413000000000     6.435000000000    44.290000000000
C                    65.092000000000     4.526000000000    45.758000000000
O                    65.959000000000     3.704000000000    45.464000000000
N                    64.595000000000     4.675000000000    46.998000000000
H                    63.894000000000     5.383000000000    47.173000000000
C                    64.961000000000     3.831000000000    48.137000000000
H                    66.042000000000     3.676000000000    48.123000000000
C                    64.613000000000     4.560000000000    49.432000000000
H                    65.160000000000     5.499000000000    49.515000000000
H                    63.548000000000     4.788000000000    49.497000000000
H                    64.872000000000     3.955000000000    50.302000000000
C                    64.285000000000     2.451000000000    48.066000000000
O                    64.947000000000     1.445000000000    48.316000000000
N                    62.979000000000     2.442000000000    47.761000000000
H                    62.517000000000     3.320000000000    47.559000000000
C                    62.080000000000     1.297000000000    47.931000000000
H                    62.576000000000     0.000000000000    48.571000000000
C                    60.796000000000     1.679000000000    48.661000000000
H                    60.193000000000     2.367000000000    48.067000000000
H                    60.176000000000     0.000000000000    48.889000000000
H                    61.018000000000     2.170000000000    49.609000000000
C                    61.783000000000     0.000000000000    46.624000000000
O                    60.783000000000     0.000000000000    46.595000000000
N                    62.636000000000     0.000000000000    45.584000000000
H                    63.451000000000     1.226000000000    45.662000000000
C                    62.436000000000     0.000000000000    44.285000000000
H                    61.529000000000     0.000000000000    43.849000000000
C                    63.580000000000     0.000000000000    43.305000000000
H                    63.393000000000     0.000000000000    42.347000000000
H                    63.705000000000     1.261000000000    43.105000000000
H                    64.527000000000     0.000000000000    43.691000000000
C                    62.215000000000    -1.571000000000    44.392000000000
O                    61.379000000000    -2.107000000000    43.665000000000
N                    62.928000000000    -2.222000000000    45.325000000000
H                    63.590000000000    -1.700000000000    45.885000000000
C                    62.797000000000    -3.646000000000    45.619000000000
H                    63.635000000000    -3.966000000000    46.238000000000
H                    62.848000000000    -4.226000000000    44.696000000000
C                    61.487000000000    -3.951000000000    46.356000000000
O                    60.737000000000    -4.817000000000    45.912000000000
N                    61.215000000000    -3.232000000000    47.460000000000
H                    61.889000000000    -2.544000000000    47.772000000000
C                    60.026000000000    -3.379000000000    48.307000000000
H                    59.985000000000    -4.424000000000    48.623000000000
C                    60.205000000000    -2.526000000000    49.560000000000
H                    60.327000000000    -1.472000000000    49.312000000000
H                    59.339000000000    -2.611000000000    50.216000000000
H                    61.078000000000    -2.840000000000    50.132000000000
C                    58.705000000000    -3.083000000000    47.574000000000
O                    57.751000000000    -3.843000000000    47.723000000000
N                    58.686000000000    -2.007000000000    46.771000000000
H                    59.505000000000    -1.411000000000    46.726000000000
C                    57.585000000000    -1.638000000000    45.881000000000
H                    56.692000000000    -1.576000000000    46.506000000000
C                    57.760000000000     0.000000000000    45.227000000000
H                    58.661000000000     0.000000000000    44.613000000000
H                    56.918000000000     0.000000000000    44.584000000000
H                    57.845000000000     0.000000000000    45.979000000000
C                    57.307000000000    -2.712000000000    44.822000000000
O                    56.137000000000    -3.011000000000    44.597000000000
N                    58.363000000000    -3.300000000000    44.228000000000
H                    59.300000000000    -3.006000000000    44.468000000000
C                    58.250000000000    -4.389000000000    43.253000000000
H                    57.570000000000    -4.031000000000    42.477000000000
C                    59.589000000000    -4.632000000000    42.562000000000
H                    59.512000000000    -5.442000000000    41.835000000000
H                    59.921000000000    -3.744000000000    42.025000000000
H                    60.367000000000    -4.905000000000    43.275000000000
C                    57.599000000000    -5.671000000000    43.814000000000
O                    56.784000000000    -6.277000000000    43.119000000000
N                    57.924000000000    -6.020000000000    45.073000000000
H                    58.614000000000    -5.474000000000    45.572000000000
C                    57.287000000000    -7.098000000000    45.842000000000
H                    57.392000000000    -8.024000000000    45.272000000000
H                    56.227000000000    -6.892000000000    45.993000000000
H                    57.769000000000    -7.216000000000    46.812000000000
"""
)

monomerB = base64encode(
"""
C  56.282 16.378 57.621
C  56.834 15.837 56.524
C  58.279 22.417 53.598
C  57.370 22.160 52.579
C  58.747 21.380 54.394
C  56.925 20.858 52.361
C  58.292 20.088 54.185
C  56.429 17.916 51.785
C  55.922 16.622 51.676
C  56.729 17.578 54.142
C  56.063 15.397 55.288
C  55.187 12.287 51.991
C  54.688 11.792 53.357
C  56.040 13.558 52.114
O  55.220 14.572 52.679
C  57.361 19.807 53.181
C  56.838 18.417 53.025
C  56.221 16.278 54.049
C  55.805 15.806 52.799
H  56.889 16.671 58.467
H  55.215 16.540 57.696
H  57.907 15.694 56.488
H  58.628 23.427 53.768
H  57.013 22.975 51.969
H  59.462 21.581 55.180
H  56.226 20.680 51.560
H  58.681 19.305 54.820
H  56.499 18.526 50.895
H  55.597 16.245 50.723
H  57.004 17.959 55.114
H  54.998 15.320 55.515
H  56.396 14.385 55.052
H  54.336 12.479 51.335
H  55.773 11.505 51.508
H  54.050 12.532 53.844
H  55.518 11.575 54.031
H  56.413 13.855 51.133
H  56.912 13.374 52.744
H  54.103 10.878 53.251
"""
)

job_params = {
  "name": "fsapt-test",
  "version": "v1",
  "kind": "FSAPTCalculation",
  "parameters": {
        "molecule_a": {
            "base64data": monomerA,
            "filetype": "xyz",
            "params": {
                "charge": 0,
            }
        },
        "molecule_b": {
            "base64data": monomerB,
            "filetype": "xyz",
            "params": {
                "charge": 0,
            }
        },
        "system": {
            "params": {
                "methodname": "hf",
                "basisname": "jun-cc-pvdz",
                "jkfit_basisname": "jun-cc-pvdz-jkfit",
                "k_grid_scheme": "GRID1",
                "threshold_pq": 1e-12
            }
        },
        "jk_builder": {
#            "type": "core_dfjk",
            "type": "dfj_grid_k",
#            "type": "numerical_jk",
            "params": {}
        },
        "hf": {
            "params": {
                "g_convergence": 1.0e-6
            }
        }
  },
  "resources": {
    "gpu_type": "a100",
    "gpu_count": 1
  },
  "metadata": {"workflow_timeout": workflow_timeout, "task_timeout": task_timeout},
}

headers = {
    "x-api-key": os.environ["PM_API_KEY"],
    "accept": "application/json",
    "content-type": "application/json",
}

client = httpx.Client(base_url=base_url, headers=headers)

payload = job_params
jobname = payload["name"]
print(f"Submitting {jobname}...", end="")
response = client.post("/v0/workflows", json=payload)
response.raise_for_status()
with open(f"{foldername}/{jobname}_submitted.json", "w") as fp:
    fp.write(json.dumps(response.json()))
workflow_id = response.json()["id"]
print("done!")

workflow = wait_for_workflows_to_complete(
    client=client,
    workflow_ids=[workflow_id],
    log_events=["STATE_CHANGES"],
    timeout=3600,
)[workflow_id]
print(f"Workflow completed with status: {workflow['status']}")

response = client.get(f"/v0/workflows/{workflow_id}").json()
with open(f"{foldername}/{jobname}_status.json", "w") as fp:
    fp.write(json.dumps(response))
name = response["name"]
timetaken = response["duration_seconds"]
print(f"Name: {name}, time taken: {timetaken:.2f}s")

response = client.get(f"/v0/workflows/{workflow_id}/results").json()
with open(f"{foldername}/{jobname}_results.json", "w") as fp:
    fp.write(json.dumps(response))

response = client.get(
    f"/v0/workflows/{workflow_id}/results/download", follow_redirects=True
)
with open(f"{foldername}/{jobname}_results.zip", "wb") as fp:
    fp.write(response.content)

response = client.get(f"/v0/workflows/{workflow_id}/results").json()

Eelst = 627.5095 * response['results']['fsapt']['scalars']['Eelst']
Eexch = 627.5095 * response['results']['fsapt']['scalars']['Eexch']
EindAB = 627.5095 * response['results']['fsapt']['scalars']['EindAB']
EindBA = 627.5095 * response['results']['fsapt']['scalars']['EindBA']
Edisp = 627.5095 * response['results']['fsapt']['scalars']['Edisp']
Esapt = 627.5095 * response['results']['fsapt']['scalars']['Esapt']

print('')
print('SAPT Analysis (kcal / mol)')
print('')
print('    Elst     Exch    IndAB    IndBA     Disp    Total')
print('%8.3lf %8.3lf %8.3lf %8.3lf %8.3lf %8.3lf' % (Eelst, Eexch, EindAB, EindBA, Edisp, Esapt))
print('')

