import math

def flow_forecast(done: list, backlog: int, today: int, window: int) -> dict:
if window <= 0:
raise ValueError("Некоректне вікно")
if backlog < 0:
raise ValueError("Некоректний обсяг черги")

for idx, (start, end) in enumerate(done, start=1):
    if end < start:
        raise ValueError(f"Некоректний елемент: {idx}")
        
window_elements = []
for start, end in done:
    if today - window < end <= today:
        window_elements.append((start, end))
        
if not window_elements:
    raise ValueError("Немає завершених елементів у вікні")
    
count = len(window_elements)
cycles = [end - start + 1 for start, end in window_elements]

avg_cycle_days = round(sum(cycles) / count, 1)
throughput_per_week = round(count * 7 / window, 2)
avg_wip = round(sum(cycles) / window, 2)

if backlog == 0:
    forecast_days = 0
else:
    forecast_days = (backlog * window + count - 1) // count
    
return {
    "avg_cycle_days": avg_cycle_days,
    "throughput_per_week": throughput_per_week,
    "avg_wip": avg_wip,
    "forecast_days": forecast_days
}
