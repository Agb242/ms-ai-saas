import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const Conversations: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Conversations
        </Typography>
        <Typography variant="body1">
          Liste des conversations SMS
        </Typography>
      </Paper>
    </Box>
  );
};

export default Conversations; 