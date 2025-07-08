import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { Container, Grid, Box, Typography, Paper, CircularProgress } from '@mui/material';
import SignalCard from './SignalCard';
import Chart from './Chart';
import { fetchCurrentSignals, fetchSignalHistory, fetchCurrentInsight } from '../services/api';

const Dashboard = () => {
  // Fetch current signals
  const { 
    data: signalData, 
    isLoading: isLoadingSignals, 
    isError: isSignalError 
  } = useQuery('currentSignals', fetchCurrentSignals, {
    refetchInterval: 300000, // 5 minutes
  });

  // Fetch signal history
  const {
    data: historyData,
    isLoading: isLoadingHistory,
  } = useQuery('signalHistory', () => fetchSignalHistory(30), {
    refetchInterval: 3600000, // 1 hour
  });

  // Fetch current AI insight
  const {
    data: insightData,
    isLoading: isLoadingInsight,
    isError: isInsightError
  } = useQuery('currentInsight', fetchCurrentInsight, {
    refetchInterval: 300000, // 5 minutes
  });

  if (isLoadingSignals || isLoadingInsight) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (isSignalError || isInsightError) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <Typography variant="h5" color="error">
          Error loading market data. Please try again later.
        </Typography>
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom component="h1">
        Market Pulse Dashboard
      </Typography>
      
      {/* Overall Signal */}
      <Paper 
        elevation={3} 
        sx={{ 
          p: 3, 
          mb: 4, 
          bgcolor: signalData?.overall_signal === 'Green' ? 'success.dark' : 
                  signalData?.overall_signal === 'Red' ? 'error.dark' : 
                  'warning.dark'
        }}
      >
        <Typography variant="h5" component="h2">
          Overall Market Signal: {signalData?.overall_signal}
        </Typography>
        <Typography variant="body1" sx={{ mt: 1 }}>
          Last Updated: {signalData?.timestamp ? new Date(signalData.timestamp).toLocaleString() : 'N/A'}
        </Typography>
      </Paper>
      
      {/* Market Insight from AI */}
      <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Market Insight
        </Typography>
        <Typography variant="body1" paragraph>
          {insightData?.content || 'No insight available.'}
        </Typography>
      </Paper>
      
      {/* Signal Cards */}
      <Grid container spacing={4} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <SignalCard 
            title="Market Breadth" 
            signal={signalData?.market_breadth_signal || 'Unknown'} 
            description="SPY vs RSP performance" 
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <SignalCard 
            title="Valuation" 
            signal={signalData?.valuation_signal || 'Unknown'} 
            description="P/E ratio vs historical norms" 
          />
        </Grid>
        <Grid item xs={12} md={4}>
          <SignalCard 
            title="Volatility" 
            signal={signalData?.volatility_signal || 'Unknown'} 
            description="VIX levels" 
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <SignalCard 
            title="Liquidity" 
            signal={signalData?.liquidity_signal || 'Unknown'} 
            description="M2 supply and Fed balance sheet" 
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <SignalCard 
            title="Macro" 
            signal={signalData?.macro_signal || 'Unknown'} 
            description="GDP and ISM Manufacturing" 
          />
        </Grid>
      </Grid>
      
      {/* Chart Section */}
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h5" component="h2" gutterBottom>
          Signal History (30 Days)
        </Typography>
        {historyData ? (
          <Chart historyData={historyData} />
        ) : (
          <Typography>No historical data available</Typography>
        )}
      </Paper>
    </Container>
  );
};

export default Dashboard;
