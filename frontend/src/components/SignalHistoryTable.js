import React from 'react';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  Paper,
  Typography,
  Tooltip
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';
import { format } from 'date-fns';

// Signal emoji mapping
const signalEmoji = {
  'Green': '🟢',
  'Yellow': '🟡',
  'Red': '🔴',
};

// Signal readable labels
const signalLabels = {
  'market_breadth_signal': 'Market Breadth',
  'valuation_signal': 'Valuation',
  'volatility_signal': 'Volatility',
  'liquidity_signal': 'Liquidity',
  'macro_signal': 'Macro',
  'overall_signal': 'Overall Signal'
};

// Render trend icon based on slope value
const renderTrendIcon = (slope) => {
  if (!slope && slope !== 0) return null;
  
  if (slope > 0.1) {
    return <TrendingUpIcon sx={{ color: 'success.main' }} />;
  } else if (slope < -0.1) {
    return <TrendingDownIcon sx={{ color: 'error.main' }} />;
  } else {
    return <TrendingFlatIcon sx={{ color: 'warning.main' }} />;
  }
};

const SignalHistoryTable = ({ historyData }) => {
  if (!historyData || !historyData.signals || historyData.signals.length === 0) {
    return (
      <Typography variant="body1" sx={{ my: 2 }}>
        No historical data available
      </Typography>
    );
  }
  
  const signals = historyData.signals;
  const trends = historyData.trends || {};
  
  // Format dates for column headers
  const dates = signals.map(item => {
    return {
      date: new Date(item.timestamp),
      formatted: format(new Date(item.timestamp), 'MMM d')
    };
  });
  
  // All signal types to display
  const signalTypes = [
    'market_breadth_signal',
    'valuation_signal',
    'volatility_signal',
    'liquidity_signal',
    'macro_signal',
    'overall_signal'
  ];
  
  return (
    <TableContainer component={Paper} sx={{ mt: 3, mb: 4 }}>
      <Typography variant="h6" component="h3" sx={{ p: 2, pb: 1 }}>
        📊 7-Day Signal History
      </Typography>
      
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Metric</TableCell>
            {dates.map((date) => (
              <TableCell key={date.formatted} align="center">
                {date.formatted}
              </TableCell>
            ))}
            <TableCell align="center">Trend</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {signalTypes.map((signalType) => (
            <TableRow key={signalType} hover>
              <TableCell component="th" scope="row">
                {signalLabels[signalType]}
              </TableCell>
              
              {/* Signal cells for each date */}
              {signals.map((item) => (
                <TableCell 
                  key={`${signalType}-${item.id}`} 
                  align="center"
                  sx={{
                    fontSize: '1.2rem',
                    bgcolor: 
                      item[signalType] === 'Red' ? 'error.dark' :
                      item[signalType] === 'Yellow' ? 'warning.dark' :
                      'success.dark',
                    opacity: 0.7
                  }}
                >
                  {signalEmoji[item[signalType]]}
                </TableCell>
              ))}
              
              {/* Trend cell */}
              <TableCell align="center">
                <Tooltip 
                  title={`Trend value: ${trends[signalType] || 'N/A'}`}
                  placement="right"
                >
                  <span>
                    {renderTrendIcon(trends[signalType])}
                    {trends[signalType] ? ` ${trends[signalType]}` : 'N/A'}
                  </span>
                </Tooltip>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default SignalHistoryTable;
