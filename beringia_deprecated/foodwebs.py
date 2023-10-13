
x={"population": 10, "reproduction_rate":0.06, "name":"spider"}

y1= dict(BulkFaunas={
    dict(name="aphid", population=1.0, reproduction_rate=0.1, starvation_rate=0.3, feeding_rate=0.1,
         emigration_rate=0.1, prey="plant", location=None),
    dict(name="spider", population=1.0, reproduction_rate=0.04, starvation_rate=0.3, feeding_rate=0.1,
         emigration_rate=0.1, prey="aphid", location=None)
}, BulkFaunasD={
    dict(name="shrew", population=20, reproduction_rate=0.08, starvation_rate=0.3, feeding_rate=0.1,
         emigration_rate=0.25, prey="spider", location=None),
    dict(name="ferret", population=2, reproduction_rate=0.02, starvation_rate=0.2, feeding_rate=0.1,
         emigration_rate=0.35, prey="shrew", location=None)
})

y={"BulkFaunas":{
    {"name": "aphid",
    "population":1.0,
    "reproduction_rate":0.1,
    "starvation_rate":0.3,
    "feeding_rate":0.1,
    "emigration_rate":0.1,
    "prey":"plant",
    "location":None},
    {"name": "spider",
    "population":1.0,
    "reproduction_rate":0.04,
    "starvation_rate":0.3,
    "feeding_rate":0.1,
    "emigration_rate":0.1,
    "prey":"aphid",
    "location":None}
    },
"BulkFaunasD":{
    {"name": "shrew",
    "population":20,
    "reproduction_rate":0.08,
    "starvation_rate":0.3,
    "feeding_rate":0.1,
    "emigration_rate":0.1,
    "prey":"spider",
    "location":None},
    {"name": "ferret",
    "population":2,
    "reproduction_rate":0.02,
    "starvation_rate":0.2,
    "feeding_rate":0.1,
    "emigration_rate":0.1,
    "prey":"shrew",
    "location":None}
}}