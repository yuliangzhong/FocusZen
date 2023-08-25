<p align="center">
  <img width="444" alt="Screenshot" src="https://github.com/yuliangzhong/FocusZen/assets/39910677/f9f6cba5-b08e-4bb6-aaae-62070a0bbbaf">
</p>

# FocusZen: Amplify Your Focus. Amplify Your Productivity.

In a world overflowing with distractions, staying focused matters more than ever. That's where FocusZen comes in – your ultimate tool to conquer tasks.

### FocusZen uses **four techniques** to help you focus better:

1. **Single Task Spotlight**: Define your daily schedule in .txt or .md files (e.g. example_schedule.md). FocusZen only displays you the current task, so you can focus on one thing at a time.
2. **Countdown Mastery**: Feel the power of countdowns. See your remaining time visually, feel a rush to finish tasks, and keep your mind on track.
3. **Pomodoro Tick**: Try the famous Pomodoro technique. 25 minutes of pure focus, followed by a 5-minute break. Stay productive and keep a healthy work-life balance.
4. **Idea Capture**: Worried of losing inspirations, but feeling distractive of keeping them in mind? With FocusZen, Capture your bright thoughts effortlessly and put them down before they vanish. You can press "save" button to store them in a notebook, or just keep them in the text widget. Now, you stay on track again while never losing those valuable flashes of insight.

### A note from the author:
"Zen," deeply rooted in Chinese culture, represents a philosophy of balance and harmony. Drawing from ancient wisdom, it encapsulates the art of living in the present moment and embracing simplicity to attain a serene mind. Just as a tranquil garden reflects the essence of Zen, FocusZen captures this essence digitally. Rediscover the serenity of Chinese wisdom in a modern context with FocusZen – 

**Where Distractions Dissolve, and Zen Emerges.**

## Easy to play!
1. Download the repo to local
```git clone git@github.com:yuliangzhong/FocusZen.git```
2. Launch the app by simply running python
```python3 FocusZen.py```
* install dependencies if needed

## Advanced usage: Automatic launching after reboot
1. Open terminal and type 
```crontab -e```
2. Add the following line to the end of the file
```@reboot sleep 30 && DISPLAY=:0 /usr/bin/python3 /exact/path/to/FocusZen.py```
* If it doesn't work properly, you can add ```>> /path/where/you/like/FocusZenOutputLog.txt 2>&1``` to the end of above command for debugging.
3. `ctrl + o` to save, `enter`, and `ctrl + x` to exit
4. Check if the cron job is added by 
```crontab -l```

Enjoy :)
