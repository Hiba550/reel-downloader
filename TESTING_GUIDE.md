# Testing Guide - PWA Two-Mode System

## Quick Start
1. Start the Flask app: `python app.py`
2. Open in browser: `http://localhost:5050`
3. For mobile testing: Use ngrok or similar to get HTTPS URL

## Test Scenarios

### 1. Background Mode (Share from Instagram)
**Setup:**
- Install PWA on Android device
- Open Instagram app
- Find a public Reel

**Steps:**
1. Tap Share button on Reel
2. Select "Reel DL" from share sheet
3. **Expected**: Small badge appears at top within 200ms
4. **Expected**: Badge shows "📥 Downloading Reel… processing"
5. **Expected**: Badge auto-dismisses after ~1.4s
6. **Expected**: Download starts automatically
7. **Expected**: Redirects to result page
8. **Expected**: Auto-download countdown begins (3s)

**Verify:**
- ✅ Badge appears at top (not center)
- ✅ Badge has Instagram gradient background
- ✅ White text is readable (contrast ≥4.5:1)
- ✅ Badge doesn't block content
- ✅ No backdrop/dimming
- ✅ Auto-dismisses smoothly
- ✅ Download initiates without user action
- ✅ Session consumed (refresh doesn't re-show badge)

### 2. Normal Mode (Direct Open)
**Setup:**
- Open PWA directly (not via share)
- Or open in desktop browser

**Steps:**
1. Paste Instagram Reel URL in input
2. Click "Download" button
3. **Expected**: Form submits, shows loading spinner
4. **Expected**: Redirects to result page
5. **Expected**: Auto-download countdown (3s)
6. **Expected**: Video preview loads
7. **Expected**: Metadata displays

**Verify:**
- ✅ No badge/overlay on initial load
- ✅ Input accepts valid URLs only
- ✅ Loading spinner shows on submit button
- ✅ Result page renders correctly
- ✅ Video plays in preview
- ✅ Download link works
- ✅ Copy link button copies to clipboard
- ✅ Auto-download can be toggled off

### 3. Bottom Sheet (Share with background_mode=false)
**To test:** Temporarily set `background_mode = False` in app.py share-target handler

**Steps:**
1. Share Reel from Instagram to PWA
2. **Expected**: Bottom sheet slides up from bottom
3. **Expected**: Shows "Ready to Download" title
4. **Expected**: Displays URL preview
5. **Expected**: "Download Now" and "Cancel" buttons visible
6. **Expected**: Auto-submits after 2.8s if no action
7. **Expected**: Can click "Download Now" to skip countdown
8. **Expected**: Can click "Cancel" or backdrop to dismiss

**Verify:**
- ✅ Sheet slides up smoothly (280ms)
- ✅ Backdrop dims page (50% opacity)
- ✅ Handle bar visible at top
- ✅ Sheet height appropriate (55-70% viewport)
- ✅ Buttons are tappable (44px min height)
- ✅ Sheet dismisses on backdrop click
- ✅ Focus trapped in sheet (accessibility)
- ✅ Escape key closes sheet

### 4. Error Handling
**Test Cases:**

#### Invalid URL
1. Enter non-Instagram URL
2. **Expected**: Error alert appears
3. **Expected**: "Please enter a valid Instagram URL"

#### Private Reel
1. Paste URL of private Reel
2. **Expected**: Instagram error returned
3. **Expected**: Error message displayed

#### Non-video Post
1. Paste URL of image post (not Reel)
2. **Expected**: "This post does not contain a video"

#### Rate Limit
1. Download 5+ Reels quickly
2. **Expected**: Rate limit error from Instagram
3. **Expected**: User-friendly error message

**Verify:**
- ✅ Error messages are clear and concise
- ✅ No technical jargon
- ✅ Red/warning styling applied
- ✅ Form remains functional after error

### 5. Accessibility Tests

#### Keyboard Navigation
1. Tab through all interactive elements
2. **Expected**: Focus visible on all buttons/inputs
3. **Expected**: Enter key submits form
4. **Expected**: Escape closes overlays

#### Screen Reader
1. Enable VoiceOver (iOS) or TalkBack (Android)
2. Navigate through app
3. **Expected**: Badge announces as status
4. **Expected**: All buttons have labels
5. **Expected**: Form labels are read correctly

#### Reduced Motion
1. Enable "Reduce motion" in OS settings
2. Navigate app
3. **Expected**: Animations are disabled/simplified
4. **Expected**: Transitions instant or very brief

**Verify:**
- ✅ All interactive elements keyboard-accessible
- ✅ Focus indicators visible
- ✅ ARIA labels present where needed
- ✅ Status updates announced
- ✅ Color contrast meets WCAG AA (4.5:1)
- ✅ Reduced motion respected

### 6. Mobile Responsiveness

#### Small Phone (iPhone SE, 375px)
- ✅ Badge fits within screen width
- ✅ Form inputs stack vertically
- ✅ Buttons full-width
- ✅ Sheet doesn't overflow
- ✅ Text remains readable

#### Medium Phone (iPhone 14, 390px)
- ✅ Layout comfortable
- ✅ Touch targets ≥44px
- ✅ Spacing appropriate

#### Large Phone (iPhone Pro Max, 430px)
- ✅ Content doesn't feel cramped
- ✅ Max-width prevents over-stretching

#### Tablet (iPad, 768px)
- ✅ Sheet max-width applied
- ✅ Layout adapts to landscape
- ✅ Metadata grid shows multiple columns

### 7. PWA Installation

#### Android Chrome
1. Visit site 2+ times
2. **Expected**: Install prompt appears
3. Install PWA
4. **Expected**: Icon added to home screen
5. Launch from home screen
6. **Expected**: Opens in standalone mode
7. **Expected**: No browser chrome visible
8. **Expected**: Share target available in system share sheet

#### iOS Safari
1. Tap Share → "Add to Home Screen"
2. **Expected**: Custom icon used
3. **Expected**: Custom title "Reel DL"
4. Launch PWA
5. **Expected**: Opens in standalone
6. **Expected**: Status bar styled correctly

**Verify:**
- ✅ Icon displays correctly (192x192, 512x512)
- ✅ Splash screen shows brand color
- ✅ Theme color applied to status bar
- ✅ Display mode is "standalone"
- ✅ Share target registered (Android)

### 8. Session & State Management

#### Refresh After Share
1. Share Reel to PWA
2. Badge appears
3. Immediately refresh page
4. **Expected**: Badge does NOT reappear
5. **Expected**: Form is clean/empty

#### Back Navigation
1. Download Reel → result page
2. Click browser back button
3. **Expected**: Returns to homepage
4. **Expected**: Form is empty
5. **Expected**: No overlay shown

#### Multiple Downloads
1. Download Reel A
2. Click "New Download"
3. Download Reel B
4. **Expected**: Each result page isolated
5. **Expected**: No state leakage

**Verify:**
- ✅ Session consumed on first use
- ✅ Refresh is safe (no loops)
- ✅ Back button works correctly
- ✅ No stale data shown

### 9. Network Conditions

#### Slow 3G
1. Throttle network to Slow 3G
2. Download Reel
3. **Expected**: Loading spinner shows
4. **Expected**: Process completes (may take longer)
5. **Expected**: User informed of progress

#### Offline
1. Disable network
2. Open PWA
3. **Expected**: Offline banner/message
4. **Expected**: Download button disabled
5. Re-enable network
6. **Expected**: App recovers

#### Flaky Connection
1. Enable network intermittently during download
2. **Expected**: Retry logic handles failures
3. **Expected**: User notified of issues

**Verify:**
- ✅ Loading states clear
- ✅ Timeouts handled gracefully
- ✅ Retry options available
- ✅ Offline state indicated

### 10. Dark Mode

#### Auto (System)
1. Set device to light mode
2. **Expected**: App uses light theme
3. Switch device to dark mode
4. **Expected**: App switches to dark theme

#### Manual Toggle
1. Click theme toggle button
2. **Expected**: Theme switches immediately
3. **Expected**: Preference saved
4. Reload page
5. **Expected**: Theme persisted

**Verify:**
- ✅ Colors invert correctly
- ✅ Contrast maintained
- ✅ Gradients adjusted
- ✅ Text readable in both modes
- ✅ Icons switch appropriately

## Quick Checklist

### Before Release
- [ ] Share from Instagram works
- [ ] Badge auto-dismisses (1.4s)
- [ ] Bottom sheet slides correctly (280ms)
- [ ] Direct download functional
- [ ] Error messages clear
- [ ] Mobile responsive
- [ ] PWA installs correctly
- [ ] Accessibility passes
- [ ] Dark mode works
- [ ] Session management safe
- [ ] No console errors
- [ ] Service worker registered
- [ ] Manifest valid

### Performance
- [ ] First load < 3s
- [ ] Badge animation smooth (60fps)
- [ ] Sheet animation smooth (60fps)
- [ ] Video preview loads quickly
- [ ] No layout shifts (CLS < 0.1)
- [ ] Lighthouse score > 90

### Browser Testing
- [ ] Chrome/Edge 93+ (Android)
- [ ] Safari 15.4+ (iOS)
- [ ] Firefox 120+ (limited)
- [ ] Samsung Internet

## Bug Report Template
```
**Issue:** [Brief description]
**Environment:** [Browser, OS, Device]
**Steps to Reproduce:**
1. 
2. 
3. 

**Expected:** 
**Actual:** 
**Screenshots:** [If applicable]
**Console Errors:** [If any]
```

## Notes
- Always test on real devices, not just emulators
- Use HTTPS for testing share-target (required)
- Clear cache between major changes
- Test in incognito for fresh sessions
- Monitor console for errors/warnings
