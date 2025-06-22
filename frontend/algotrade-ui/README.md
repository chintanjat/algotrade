# AlgoTrade UI

A modern React-based trading dashboard for the AlgoTrade algorithmic trading platform.

## 🎨 Features

- **Modern UI**: Built with React, TypeScript, and Ant Design
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark Mode Support**: Built-in dark/light theme switching
- **Real-time Data**: Live portfolio updates and position tracking
- **Strategy Management**: Enable/disable and configure trading strategies
- **Performance Analytics**: P&L charts and performance metrics
- **Trade History**: Complete trade log with filtering and search

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks and functional components
- **TypeScript** - Type-safe development
- **Ant Design** - Enterprise-grade UI components
- **TailwindCSS** - Utility-first CSS framework
- **Recharts** - Beautiful charts and data visualization
- **React Router** - Client-side routing
- **Axios** - HTTP client for API communication

## 📁 Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── SidebarNav.tsx   # Navigation sidebar
│   ├── Topbar.tsx       # Top navigation bar
│   ├── DashboardCards.tsx # Portfolio summary cards
│   ├── StrategyDetailsPanel.tsx # Strategy management
│   ├── ActivePositionsTable.tsx # Open positions table
│   ├── PnLPerformanceChart.tsx # Performance chart
│   └── ErrorCenter.tsx  # System alerts
├── pages/               # Page components
│   ├── Dashboard.tsx    # Main dashboard
│   ├── Strategies.tsx   # Strategy management
│   ├── Positions.tsx    # Active positions
│   ├── Trades.tsx       # Trade history
│   └── Performance.tsx  # Performance analytics
├── utils/               # Utility functions
├── types/               # TypeScript type definitions
└── index.css           # Global styles and TailwindCSS
```

## 🚀 Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend server running (see backend README)

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend/algotrade-ui
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

## 🎯 Components Overview

### Core Components

#### SidebarNav
- Navigation menu with dashboard sections
- Shows current page and version info
- Collapsible design for mobile

#### Topbar
- Portfolio value and broker status
- Available and allocated capital display
- Quick action buttons (notifications, settings, profile)

#### DashboardCards
- Portfolio summary cards
- Total value, available capital, allocated capital
- P&L display with color coding

#### StrategyDetailsPanel
- List of trading strategies
- Enable/disable toggles
- Signal source configuration
- Strategy parameters display

#### ActivePositionsTable
- Real-time position data
- P&L calculations and percentages
- Position management actions
- Responsive table design

#### PnLPerformanceChart
- Interactive line chart
- Historical P&L data
- Custom tooltips and formatting
- Responsive design

#### ErrorCenter
- System alerts and notifications
- Error, warning, and info messages
- Collapsible interface
- Dismiss functionality

## 🎨 Styling

### TailwindCSS Configuration

The project uses a custom TailwindCSS configuration with:

- **Custom Colors**: Primary, success, warning, danger color schemes
- **Dark Mode**: Built-in dark mode support
- **Custom Animations**: Fade-in, slide-up, and pulse animations
- **Typography**: Inter font for UI, JetBrains Mono for code

### Ant Design Integration

Custom styling overrides for Ant Design components:

- Dark mode compatibility
- Consistent color schemes
- Custom component styling
- Responsive design adjustments

## 🔌 API Integration

The frontend communicates with the backend via HTTP API:

### Base Configuration
- **Proxy**: Configured to forward requests to `http://localhost:5000`
- **CORS**: Handled by backend HTTP bridge
- **Error Handling**: Centralized error handling and display

### API Endpoints

#### Account & Portfolio
- `GET /api/account` - Account summary
- `GET /api/positions` - Open positions
- `GET /api/performance` - Performance metrics

#### Strategies
- `GET /api/strategies` - List strategies
- `POST /api/strategy/toggle` - Toggle strategy
- `POST /api/strategy/create` - Create strategy
- `POST /api/strategy/update` - Update strategy

#### Trading
- `POST /api/order` - Place order
- `GET /api/trades` - Trade history
- `GET /api/signals` - Trading signals

## 📱 Responsive Design

The application is fully responsive with:

- **Mobile First**: Designed for mobile devices first
- **Breakpoints**: TailwindCSS responsive breakpoints
- **Flexible Layout**: Adaptive grid and flexbox layouts
- **Touch Friendly**: Optimized for touch interactions

## 🌙 Dark Mode

Built-in dark mode support:

- **System Preference**: Automatically detects system theme
- **Manual Toggle**: User can override system preference
- **Persistent**: Theme choice is saved in localStorage
- **Consistent**: All components support dark mode

## 🔧 Development

### Code Style

- **TypeScript**: Strict type checking enabled
- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting
- **Component Structure**: Functional components with hooks

### State Management

- **React Hooks**: useState, useEffect, useContext
- **Local State**: Component-level state management
- **API State**: Centralized API state handling
- **Form State**: Ant Design form management

### Performance

- **Code Splitting**: Route-based code splitting
- **Lazy Loading**: Components loaded on demand
- **Memoization**: React.memo for expensive components
- **Optimization**: Bundle size optimization

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch
```

## 📦 Build & Deploy

### Development Build
```bash
npm run build
```

### Production Build
```bash
npm run build
```

### Environment Variables

Create a `.env` file for environment-specific configuration:

```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENVIRONMENT=development
```

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection**: Ensure backend server is running on port 5000
2. **CORS Errors**: Check backend CORS configuration
3. **Build Errors**: Clear node_modules and reinstall dependencies
4. **TypeScript Errors**: Check type definitions and imports

### Debug Mode

Enable debug mode for detailed logging:

```bash
REACT_APP_DEBUG=true npm start
```

## 📝 License

This project is part of the AlgoTrade platform.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Check the documentation
- Review the backend README
- Open an issue on GitHub 