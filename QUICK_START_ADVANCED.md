# Quick Start: Advanced Features

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python Leafy.py
```

---

## Feature Highlights

### Database Features

**Automatic**:
- All commands logged to database automatically
- All responses cached in database
- Settings saved to database when changed

**Manual**:
- Save notes via voice: "Save note [title] [content]"
- View history via GUI button or "Show history" command
- Access via settings panel

### Caching Features

**Automatic**:
- Wikipedia searches cached for 7 days
- Calculations cached for 30 days
- News cached for 1 day

**Manual**:
- Clear cache in Settings → System → Clear Cache button
- Manage cache TTL in `cache.py` (line 15-19)

**Impact**:
```
First "What is Python" → 800ms (API call)
Second "What is Python" → 0ms (from cache)
Third "What is Python" → 0ms (from cache)
```

### Settings GUI

**How to Open**:
1. Click the Settings button in main window
2. Adjust any settings in the tabs
3. Click "Apply" to save

**Available Settings**:

| Tab | Options |
|-----|---------|
| Audio | Speech rate, volume, voice, language, microphone |
| Appearance | Theme, font size, window size, timestamps, notifications |
| System | Auto-start, minimize to tray, logging, caching |
| Advanced | Database stats, backup/restore, clear history, debug |

**Example**:
```
1. Click Settings
2. Go to Audio tab
3. Move Speech Rate slider to 200
4. Move Volume slider to 0.8
5. Click Apply
6. Leafy now speaks faster and louder!
```

### Database Insights

**View Statistics**:
1. Click Settings → Advanced tab
2. See database stats (notes count, command count, cache size)
3. Export current stats

**Backup Your Data**:
1. Click Settings → Advanced tab
2. Click "Backup Database"
3. File saved to `data/backups/leafy_backup_TIMESTAMP.db`

**Restore from Backup**:
1. Click Settings → Advanced tab
2. Click "Restore Database"
3. Select backup file to restore

---

## Common Commands

### Using the Database

```
"Save note team meeting Friday at 10 AM"
"Search my notes"
"Show history"
"Clear command history"
```

### Using the Cache

```
"What is artificial intelligence"         # API call ~1000ms
"What is artificial intelligence"         # Cache ~10ms
"Tell me about machine learning"          # API call ~1000ms
```

### Using Settings

```
"Open settings"  # Opens GUI settings window
```

---

## Performance Tips

### Maximize Caching

Ask similar questions to reuse cache
Wikipedia searches cached for 7 days
Calculations cached for 30 days
Clear cache when you need fresh data

### Optimize Settings

Reduce speech rate if too fast
Increase volume if too quiet
Enable caching for faster responses
Use compact window size on small screens

### Monitor Database

Check database stats regularly
Backup before major updates
Clear old history if database grows large
Review logs for errors

---

## Troubleshooting

### Settings Won't Save

**Issue**: Change setting but it reverts
**Solution**: Click "Apply" button in settings window

### Cache Not Working

**Issue**: Getting same query again takes long time
**Solution**: 
1. Check cache is enabled in Settings
2. Clear cache and try again
3. Check database is writable

### Database Error

**Issue**: "Database is locked"
**Solution**: Close other instances of Leafy

### Settings Window Won't Open

**Issue**: Clicking settings button does nothing
**Solution**: Check terminal for errors, ensure Tkinter installed

---

## Advanced Configuration

### Adjust Cache TTL

Edit `cache.py` line 15-19:

```python
TTL_WIKIPEDIA = 7 * 24 * 3600      # 7 days → change number
TTL_CALCULATION = 30 * 24 * 3600   # 30 days → change number
TTL_NEWS = 1 * 24 * 3600           # 1 day → change number
```

### Change Database Location

Edit `db.py` line 12:

```python
self.db_path = Path("data/leafy.db")  # Change path here
```

### Adjust Speech Parameters

Via Settings GUI (recommended) or edit `config.py`:

```python
SPEECH_RATE = 150      # 50-300 words per minute
SPEECH_VOLUME = 0.9    # 0.0-1.0
```

---

## Use Cases

### Student Using Leafy

1. **Scenario**: Researching for essay
   - "What is photosynthesis"
   - "What is cellular respiration"
   - Later: "What is photosynthesis" (cached, instant!)
   
2. **Settings**: Increase speech rate, use light theme

3. **Database**: Save important notes for later reference

### Busy Professional

1. **Scenario**: Quick information lookups
   - "What is the capital of France"
   - "Calculate 15% of 2000"
   - "Show me today's news"

2. **Settings**: Enable minimize to tray, auto-start

3. **Database**: Backup important notes before presenting

### Home User

1. **Scenario**: General queries and entertainment
   - "Tell me a joke"
   - "What's the weather"
   - "Open Google"

2. **Settings**: Customize voice and appearance

3. **Database**: Track favorite queries and responses

---

## Testing

### Run Feature Tests

```bash
python test_advanced_features.py
```

**Expected Output**:
```
DONE: Database tests PASSED
DONE: Caching tests PASSED
DONE: Async operations tests PASSED
DONE: Settings GUI tests PASSED
DONE: Leafy integration tests PASSED

Total: 5/5 tests passed
All advanced features are working correctly!
```

---

## What's Next?

### Coming Soon
- [ ] Async operations for all API calls
- [ ] Voice command recording/playback
- [ ] Note export to PDF
- [ ] Command statistics
- [ ] User profiles

### Feedback Welcome

Issues or suggestions? Check logs or report!

---

**Happy using Leafy with advanced features!**
