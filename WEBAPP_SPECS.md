# NLM Web Application Specifications

## 1. Overview

Web interface for NotebookLM CLI tool providing full functionality through a modern, responsive UI.

**Target Users**: Researchers, students, content creators who prefer GUI over CLI
**Tech Stack Options**: 
- Option 1: FastAPI + HTMX + Tailwind CSS
- Option 5: NiceGUI

## 2. Functional Requirements

### 2.1 Authentication
- **AUTH-001**: User must authenticate via browser (similar to CLI auth flow)
- **AUTH-002**: Store credentials securely in session
- **AUTH-003**: Display authentication status in header
- **AUTH-004**: Auto-refresh tokens before expiry
- **AUTH-005**: Logout functionality to clear credentials

### 2.2 Notebook Management
- **NB-001**: List all notebooks with title, emoji, creation date
- **NB-002**: Create new notebook with title and optional emoji
- **NB-003**: Delete notebook with confirmation dialog
- **NB-004**: View notebook analytics (if available)
- **NB-005**: Search/filter notebooks by title
- **NB-006**: Sort notebooks by date, title, or last modified

### 2.3 Source Management
- **SRC-001**: List all sources in a notebook
- **SRC-002**: Add source from URL
- **SRC-003**: Add source from file upload
- **SRC-004**: Add source from text input
- **SRC-005**: Delete source with confirmation
- **SRC-006**: Rename source
- **SRC-007**: Refresh source content
- **SRC-008**: Check source freshness status
- **SRC-009**: Display source type (URL, file, text, YouTube, etc.)
- **SRC-010**: Show source metadata (size, date added, status)

### 2.4 Note Management
- **NOTE-001**: List all notes in a notebook
- **NOTE-002**: Create new note with title
- **NOTE-003**: Edit note content (markdown editor)
- **NOTE-004**: Delete note with confirmation
- **NOTE-005**: Preview note in markdown format

### 2.5 Audio Overview
- **AUD-001**: List all audio overviews for a notebook
- **AUD-002**: Create audio overview with custom instructions
- **AUD-003**: Display audio creation status (pending, processing, ready)
- **AUD-004**: Play audio directly in browser
- **AUD-005**: Download audio file
- **AUD-006**: Delete audio overview
- **AUD-007**: Share audio overview (get public link)
- **AUD-008**: Show audio duration and file size

### 2.6 Video Overview
- **VID-001**: List all video overviews for a notebook
- **VID-002**: Create video overview with custom instructions
- **VID-003**: Display video creation status
- **VID-004**: Play video directly in browser
- **VID-005**: Download video file

### 2.7 Content Generation
- **GEN-001**: Generate study guide
- **GEN-002**: Generate content outline
- **GEN-003**: Generate FAQ
- **GEN-004**: Generate glossary
- **GEN-005**: Generate timeline
- **GEN-006**: Generate briefing document
- **GEN-007**: Display generated content with markdown rendering
- **GEN-008**: Copy generated content to clipboard
- **GEN-009**: Download generated content as file
- **GEN-010**: Show generation progress/status

### 2.8 Chat Interface
- **CHAT-001**: Interactive chat with notebook context
- **CHAT-002**: Display chat history
- **CHAT-003**: Send messages with markdown support
- **CHAT-004**: Receive AI responses with markdown rendering
- **CHAT-005**: Save chat sessions
- **CHAT-006**: Load previous chat sessions
- **CHAT-007**: Clear chat history
- **CHAT-008**: Export chat as markdown

### 2.9 Artifacts
- **ART-001**: List all artifacts in a notebook
- **ART-002**: Create artifact (note, audio, report, app)
- **ART-003**: View artifact details
- **ART-004**: Rename artifact
- **ART-005**: Delete artifact

## 3. Non-Functional Requirements

### 3.1 Performance
- **PERF-001**: Page load time < 2 seconds
- **PERF-002**: API response time < 5 seconds for most operations
- **PERF-003**: Long operations (audio/video) show progress indicators
- **PERF-004**: Async operations don't block UI

### 3.2 Usability
- **UX-001**: Responsive design (mobile, tablet, desktop)
- **UX-002**: Dark mode support
- **UX-003**: Keyboard shortcuts for common actions
- **UX-004**: Toast notifications for success/error messages
- **UX-005**: Loading states for all async operations
- **UX-006**: Confirmation dialogs for destructive actions
- **UX-007**: Breadcrumb navigation
- **UX-008**: Intuitive icon usage

### 3.3 Accessibility
- **A11Y-001**: WCAG 2.1 Level AA compliance
- **A11Y-002**: Keyboard navigation support
- **A11Y-003**: Screen reader compatible
- **A11Y-004**: Proper ARIA labels
- **A11Y-005**: Sufficient color contrast

### 3.4 Security
- **SEC-001**: No credentials stored in browser localStorage
- **SEC-002**: Session-based authentication
- **SEC-003**: CSRF protection
- **SEC-004**: Input validation and sanitization
- **SEC-005**: Secure file upload handling

### 3.5 Error Handling
- **ERR-001**: User-friendly error messages
- **ERR-002**: Graceful degradation on API failures
- **ERR-003**: Retry mechanism for transient failures
- **ERR-004**: Error logging for debugging

## 4. UI/UX Design Specifications

### 4.1 Layout
```
┌─────────────────────────────────────────────────────┐
│  Header: Logo | Notebooks | Auth Status | Theme    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────┐  ┌─────────────────────────────────┐ │
│  │          │  │                                 │ │
│  │ Sidebar  │  │     Main Content Area          │ │
│  │          │  │                                 │ │
│  │ - List   │  │  Dynamic content based on      │ │
│  │ - Create │  │  selected notebook/action      │ │
│  │ - Search │  │                                 │ │
│  │          │  │                                 │ │
│  └──────────┘  └─────────────────────────────────┘ │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 4.2 Color Scheme (Modern 2025)
**Light Mode**:
- Primary: `#6366f1` (Indigo)
- Secondary: `#8b5cf6` (Purple)
- Success: `#10b981` (Green)
- Warning: `#f59e0b` (Amber)
- Error: `#ef4444` (Red)
- Background: `#ffffff`
- Surface: `#f9fafb`
- Text: `#111827`

**Dark Mode**:
- Primary: `#818cf8` (Light Indigo)
- Secondary: `#a78bfa` (Light Purple)
- Success: `#34d399` (Light Green)
- Warning: `#fbbf24` (Light Amber)
- Error: `#f87171` (Light Red)
- Background: `#0f172a` (Slate 900)
- Surface: `#1e293b` (Slate 800)
- Text: `#f1f5f9`

### 4.3 Typography
- **Headings**: Inter or Geist Sans
- **Body**: System font stack
- **Code**: JetBrains Mono or Fira Code

### 4.4 Components

#### Notebook Card
```
┌─────────────────────────────────────┐
│ 📚 Notebook Title                   │
│ Created: 2025-01-15                 │
│ Sources: 5 | Notes: 3 | Audio: 1    │
│ [View] [Edit] [Delete]              │
└─────────────────────────────────────┘
```

#### Source Item
```
┌─────────────────────────────────────┐
│ 🔗 Source Title                     │
│ Type: URL | Added: 2 days ago       │
│ Status: ✅ Fresh                    │
│ [Rename] [Refresh] [Delete]         │
└─────────────────────────────────────┘
```

#### Audio Player
```
┌─────────────────────────────────────┐
│ 🎵 Audio Overview                   │
│ Duration: 15:30 | Size: 12.5 MB     │
│ ▶️ [=========>    ] 8:45 / 15:30   │
│ [Download] [Share] [Delete]         │
└─────────────────────────────────────┘
```

### 4.5 Interactions
- **Hover**: Subtle scale/shadow effects
- **Click**: Ripple effect on buttons
- **Loading**: Skeleton screens or spinners
- **Transitions**: 200-300ms ease-in-out
- **Animations**: Subtle fade-in for new content

## 5. API Endpoints (Backend)

### 5.1 Authentication
- `POST /api/auth/login` - Initiate authentication
- `GET /api/auth/status` - Check auth status
- `POST /api/auth/logout` - Clear session

### 5.2 Notebooks
- `GET /api/notebooks` - List all notebooks
- `POST /api/notebooks` - Create notebook
- `GET /api/notebooks/{id}` - Get notebook details
- `DELETE /api/notebooks/{id}` - Delete notebook
- `GET /api/notebooks/{id}/analytics` - Get analytics

### 5.3 Sources
- `GET /api/notebooks/{id}/sources` - List sources
- `POST /api/notebooks/{id}/sources` - Add source
- `DELETE /api/sources/{id}` - Delete source
- `PUT /api/sources/{id}` - Update source
- `POST /api/sources/{id}/refresh` - Refresh source

### 5.4 Notes
- `GET /api/notebooks/{id}/notes` - List notes
- `POST /api/notebooks/{id}/notes` - Create note
- `PUT /api/notes/{id}` - Update note
- `DELETE /api/notes/{id}` - Delete note

### 5.5 Audio
- `GET /api/notebooks/{id}/audio` - List audio overviews
- `POST /api/notebooks/{id}/audio` - Create audio
- `GET /api/audio/{id}` - Get audio details
- `GET /api/audio/{id}/download` - Download audio
- `DELETE /api/audio/{id}` - Delete audio
- `POST /api/audio/{id}/share` - Share audio

### 5.6 Video
- `GET /api/notebooks/{id}/video` - List video overviews
- `POST /api/notebooks/{id}/video` - Create video
- `GET /api/video/{id}/download` - Download video

### 5.7 Generation
- `POST /api/notebooks/{id}/generate/guide` - Generate guide
- `POST /api/notebooks/{id}/generate/outline` - Generate outline
- `POST /api/notebooks/{id}/generate/faq` - Generate FAQ
- `POST /api/notebooks/{id}/generate/glossary` - Generate glossary
- `POST /api/notebooks/{id}/generate/timeline` - Generate timeline

### 5.8 Chat
- `POST /api/notebooks/{id}/chat` - Send chat message
- `GET /api/notebooks/{id}/chat/history` - Get chat history
- `DELETE /api/notebooks/{id}/chat` - Clear chat history

### 5.9 Artifacts
- `GET /api/notebooks/{id}/artifacts` - List artifacts
- `POST /api/notebooks/{id}/artifacts` - Create artifact
- `GET /api/artifacts/{id}` - Get artifact
- `PUT /api/artifacts/{id}` - Update artifact
- `DELETE /api/artifacts/{id}` - Delete artifact

## 6. Testing Requirements

### 6.1 Unit Tests
- Test all API endpoints
- Test NLM CLI wrapper functions
- Test data validation
- Test error handling
- **Coverage Target**: > 80%

### 6.2 Integration Tests
- Test complete user flows
- Test authentication flow
- Test notebook CRUD operations
- Test file upload
- Test audio/video creation

### 6.3 E2E Tests
- Test critical user journeys
- Test responsive design
- Test dark mode
- Test keyboard navigation

### 6.4 TDD Approach
1. Write failing test
2. Implement minimal code to pass
3. Refactor
4. Repeat

## 7. Project Structure

### Option 1: FastAPI + HTMX
```
nlm-web-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── models.py            # Pydantic models
│   ├── nlm_client.py        # NLM CLI wrapper
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── notebooks.py
│   │   ├── sources.py
│   │   ├── notes.py
│   │   ├── audio.py
│   │   ├── video.py
│   │   ├── generation.py
│   │   └── chat.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── notebooks/
│   │   ├── sources/
│   │   └── components/
│   └── static/
│       ├── css/
│       │   └── styles.css
│       └── js/
│           └── htmx.min.js
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_notebooks.py
│   ├── test_sources.py
│   ├── test_notes.py
│   ├── test_audio.py
│   └── test_integration.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .env.example
└── README.md
```

### Option 5: NiceGUI
```
nlm-web-nicegui/
├── app/
│   ├── __init__.py
│   ├── main.py              # NiceGUI app
│   ├── config.py
│   ├── nlm_client.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── home.py
│   │   ├── notebooks.py
│   │   ├── sources.py
│   │   ├── notes.py
│   │   ├── audio.py
│   │   └── chat.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── notebook_card.py
│   │   ├── source_list.py
│   │   ├── audio_player.py
│   │   └── chat_interface.py
│   └── state.py             # Application state
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_nlm_client.py
│   ├── test_pages.py
│   └── test_components.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
└── README.md
```

## 8. Development Phases

### Phase 1: Core Setup (Week 1)
- Project structure
- Authentication
- Basic notebook listing
- Tests for above

### Phase 2: Notebook Management (Week 2)
- Create/delete notebooks
- Notebook details view
- Tests

### Phase 3: Source Management (Week 3)
- Add/delete sources
- File upload
- Source listing
- Tests

### Phase 4: Content Generation (Week 4)
- Generate guide/outline/FAQ
- Display generated content
- Tests

### Phase 5: Audio/Video (Week 5)
- Audio creation and playback
- Video creation and playback
- Tests

### Phase 6: Chat Interface (Week 6)
- Interactive chat
- Chat history
- Tests

### Phase 7: Polish & Deploy (Week 7)
- UI refinements
- Performance optimization
- Documentation
- Deployment setup

## 9. Success Criteria

- ✅ All functional requirements implemented
- ✅ Test coverage > 80%
- ✅ All tests passing
- ✅ Responsive on mobile/tablet/desktop
- ✅ Dark mode working
- ✅ Page load < 2 seconds
- ✅ No critical accessibility issues
- ✅ Documentation complete
- ✅ Deployable with single command

## 10. Future Enhancements

- Real-time collaboration
- Notebook sharing between users
- Advanced search with filters
- Batch operations
- Export notebooks to various formats
- Integration with other tools (Notion, Obsidian)
- Mobile app (PWA)
- Offline mode
