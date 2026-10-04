# DPU Performance Studio - Frontend Documentation

## Overview

The frontend is built with React 18 and Vite, providing a professional navy-white themed user interface for analyzing audio-AI workloads.

## Technology Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Recharts** - Data visualization library
- **Lucide React** - Icon library
- **Axios** - HTTP client for API calls

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── UploadSection.jsx       # File upload interface
│   │   ├── UploadSection.css
│   │   ├── ResultsPanel.jsx        # Main results display
│   │   ├── ResultsPanel.css
│   │   ├── MetricsComparison.jsx   # Performance comparison charts
│   │   ├── MetricsComparison.css
│   │   ├── StageBreakdown.jsx      # Stage-by-stage analysis
│   │   ├── StageBreakdown.css
│   │   ├── BottleneckAnalysis.jsx  # Bottleneck detection display
│   │   ├── BottleneckAnalysis.css
│   │   ├── PlacementDecisions.jsx  # Operation placement visualization
│   │   ├── PlacementDecisions.css
│   │   ├── ConfidenceBar.jsx       # Confidence metrics display
│   │   └── ConfidenceBar.css
│   ├── App.jsx                     # Main application component
│   ├── App.css
│   ├── main.jsx                    # Application entry point
│   └── index.css                   # Global styles and theme
├── index.html
├── package.json
└── vite.config.js
```

## Theme Configuration

### Color Palette

```css
:root {
  /* Navy Colors */
  --navy-primary: #1a365d;
  --navy-secondary: #2c5282;
  --navy-dark: #0f1f3a;
  --navy-light: #4a6fa5;
  
  /* White Colors */
  --white-primary: #ffffff;
  --white-secondary: #f7fafc;
  --white-tertiary: #edf2f7;
  
  /* Accent Colors */
  --accent-blue: #3182ce;
  --accent-light-blue: #63b3ed;
  --accent-green: #38a169;
  --accent-orange: #dd6b20;
  --accent-red: #e53e3e;
  
  /* Text Colors */
  --text-primary: #1a202c;
  --text-secondary: #4a5568;
  --text-muted: #718096;
  
  /* UI Elements */
  --border-color: #e2e8f0;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
  
  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
}
```

## Components

### 1. App.jsx

**Main application component** that manages the overall state and navigation.

**Props:** None

**State:**
- `analysisResults` - Stores the complete analysis results from the API
- `isAnalyzing` - Boolean indicating if analysis is in progress
- `selectedFile` - The currently selected audio file

**Methods:**
- `handleAnalysisComplete(results)` - Callback when analysis completes
- `handleFileSelect(file)` - Callback when file is selected
- `handleReset()` - Resets the application to initial state

---

### 2. UploadSection.jsx

**File upload interface** with drag-and-drop support.

**Props:**
- `onAnalysisComplete(results)` - Callback when analysis completes
- `onFileSelect(file)` - Callback when file is selected
- `isAnalyzing` - Boolean indicating if analysis is in progress
- `setIsAnalyzing(bool)` - Function to set analyzing state

**Features:**
- Drag-and-drop file upload
- File type validation (audio/*)
- Visual feedback during upload
- Loading spinner during analysis
- Information cards explaining the process

**API Call:**
```javascript
POST http://localhost:8000/api/analyze
Content-Type: multipart/form-data
Body: FormData with audio_file
```

---

### 3. ResultsPanel.jsx

**Main results display** that orchestrates all result components.

**Props:**
- `results` - Complete analysis results object from API
- `onReset()` - Callback to reset to upload screen

**Features:**
- Summary cards with key metrics
- Download buttons for reports (Markdown & JSON)
- Navigation back to upload
- Orchestrates all sub-components

**Sub-components:**
- MetricsComparison
- StageBreakdown
- BottleneckAnalysis
- PlacementDecisions
- ConfidenceBar

---

### 4. MetricsComparison.jsx

**Performance comparison** with bar charts and tables.

**Props:**
- `cpuBaseline` - CPU baseline results
- `dpuSimulation` - DPU simulation results
- `optimizedResults` - Optimized execution results
- `comparison` - Comparison analysis results

**Charts:**
- Latency comparison (bar chart)
- Throughput comparison (bar chart)
- CPU utilization comparison (bar chart)

**Table Metrics:**
- Total Latency
- Throughput
- CPU Utilization
- Transfer Time
- Sync Time

**Library:** Recharts

---

### 5. StageBreakdown.jsx

**Stage-by-stage execution analysis** with detailed metrics.

**Props:**
- `cpuBaseline` - CPU baseline results
- `optimizedResults` - Optimized execution results

**Features:**
- Lists all execution stages
- Shows execution location (CPU/DPU/Custom)
- Displays latency, speedup, and improvement
- Shows detailed metrics for DPU stages:
  - CPU utilization
  - DPU utilization
  - Transfer time
  - Sync time
  - Confidence score

**Stages:**
1. audio_preprocessing
2. feature_extraction
3. model_inference
4. post_processing
5. output_generation

---

### 6. BottleneckAnalysis.jsx

**Bottleneck detection and analysis** display.

**Props:**
- `bottlenecks` - Bottleneck analysis results
- `cpuBaseline` - CPU baseline results

**Features:**
- Primary bottleneck identification
- Potential improvement estimates
- Detailed bottleneck list with severity indicators
- Recommendations display

**Bottleneck Types:**
- LATENCY - Stage taking too much time
- ACCELERATION_OPPORTUNITY - Stage that benefits from DPU
- SLOW_STAGE - Stage marked for custom kernel
- CPU_UTILIZATION - High CPU usage
- MEMORY - High memory usage

**Severity Levels:**
- HIGH - >40% of total time or >80% CPU
- MEDIUM - 25-40% of total time
- LOW - <25% of total time

---

### 7. PlacementDecisions.jsx

**Operation placement visualization** with decision logic.

**Props:**
- `placementDecision` - Operation placement decision results

**Features:**
- Visual summary of placement distribution
- Stage-by-stage decision details
- Reason for each placement decision
- Expected performance estimates
- Confidence scores

**Placement Types:**
- CPU - Stay on CPU (too fast for DPU overhead)
- DPU - Move to DPU (good speedup potential)
- CUSTOM_KERNEL - Custom kernel optimization (future)

**Decision Criteria:**
- Stage must be >30ms to consider DPU
- Need >2x speedup to justify DPU
- Transfer overhead must be <30% of stage time
- Custom kernel for large stages with high overhead

---

### 8. ConfidenceBar.jsx

**Measurement confidence indicators** with data source transparency.

**Props:**
- `results` - Complete analysis results

**Features:**
- Overall confidence score (0-100%)
- Breakdown by data source:
  - CPU Measurements (95% confidence)
  - DPU Simulation (80% confidence)
  - Custom Kernel Estimates (70% confidence)
- Confidence level indicators (High/Medium/Low)
- Legend explaining confidence levels

**Confidence Levels:**
- High (90-100%): Actual measurements, highly reliable
- Medium (70-89%): Simulated values, reasonably reliable
- Low (0-69%): Estimated values, requires verification

---

## State Management

The application uses React's built-in `useState` hook for state management. No external state management library is used.

**State Flow:**
```
App.jsx (parent)
  ├── UploadSection (file selection)
  └── ResultsPanel (results display)
      ├── MetricsComparison
      ├── StageBreakdown
      ├── BottleneckAnalysis
      ├── PlacementDecisions
      └── ConfidenceBar
```

## API Integration

API calls are made using Axios. The frontend is configured to proxy API requests to the backend.

**Base URL:** `http://localhost:8000`

**Main API Call:**
```javascript
const response = await axios.post(
  'http://localhost:8000/api/analyze',
  formData,
  {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }
)
```

**Report Generation:**
```javascript
// Markdown Report
const response = await fetch('http://localhost:8000/api/report/markdown', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(results)
})

// JSON Report
const response = await fetch('http://localhost:8000/api/report/json', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(results)
})
```

## Responsive Design

The application uses CSS Grid and Flexbox for responsive layout. Components adapt to different screen sizes automatically.

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## Development

### Start Development Server
```bash
cd frontend
npm run dev
```

### Build for Production
```bash
cd frontend
npm run build
```

### Preview Production Build
```bash
cd frontend
npm run preview
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Accessibility

The application follows WCAG 2.1 AA guidelines:
- Semantic HTML
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance
- Focus indicators

## Performance Optimization

- Code splitting with Vite
- Lazy loading of components
- Optimized bundle size
- Efficient re-rendering with React
- CSS-in-JS for minimal CSS overhead

## Future Enhancements

- [ ] Real-time progress updates during analysis
- [ ] Dark mode toggle
- [ ] Export to PDF
- [ ] Historical analysis comparison
- [ ] Custom configuration options
- [ ] Multi-file batch analysis
