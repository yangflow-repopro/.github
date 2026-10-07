# App captures

How the images in `design/screenshots/<screen>/` are made and what the maintainer may accept. Stage 5 of
`handbook/guides/ui-workflow.md` refers here.

## Acceptance evidence

| Method | Evidence? |
|---|---|
| The window server's compositor output of the real window: `screencapture -x -o -l <CGWindowID>` | Yes. This is the default |
| `NSView.cacheDisplay`, SwiftUI `ImageRenderer`, any render of the view tree | **Never.** They bypass the compositor and lose glass, vibrancy, system control chrome and selected-state fills, so the colours differ from the running app |
| Renders of the design files | Never (`handbook/guides/ui-workflow.md`, Screenshots) |

A degraded method may exist for machines that cannot run the default. It prints a loud warning, writes outside the
repository and its output is never committed.

## How the capture runs

The app, in Debug builds only, does the following for each state; a script outside the app calls `screencapture`.

1. Puts the window in the requested appearance (light or dark) and size, and activates it.
2. Shows a neutral, deterministic backdrop window behind it, so translucent materials look the same every time.
3. Waits for rendering to settle.

Requirements on the machine:

- The Screen Recording permission for the application that runs the script (Terminal, the agent host).
- An unlocked, awake display, with the capture instance frontmost.
- A locked screen makes the capture fail. The agent stops and asks the maintainer to unlock it. It never falls back
  silently to another method.

## What each kind of surface needs

| Surface | How it is captured |
|---|---|
| Window | `screencapture -l` of the window |
| Sheet, system alert | The window with the sheet attached |
| System panel (About), other separate windows | Their own window id |
| Menu | Cannot be captured. Describe it in the ledger notes |
| Menu bar popover | Cannot be opened programmatically. Capture the real view tree in a normal window and write the limits (no popover chrome, no menu bar) in the ledger notes |

## Demo scenarios and Release builds

- Demo scenarios exist in `DEBUG` only. They stub the network, permissions and the Keychain, so every state is
  reproducible and nothing real is touched.
- A Release build contains no capture code and no demo scenario. Verify with `strings` and `nm` on the Release
  binary before a release.
- Capturing never changes the maintainer's saved settings (`handbook/core/agents.md`, rule 10).
