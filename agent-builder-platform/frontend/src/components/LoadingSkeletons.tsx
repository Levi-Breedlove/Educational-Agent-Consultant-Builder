import { Box, Skeleton, Paper, Stack } from '@mui/material'

export const ChatMessageSkeleton = () => (
  <Box sx={{ mb: 2 }}>
    <Stack direction="row" spacing={2} alignItems="flex-start">
      <Skeleton variant="circular" width={40} height={40} />
      <Box sx={{ flex: 1 }}>
        <Skeleton variant="text" width="30%" height={24} />
        <Skeleton variant="rectangular" width="100%" height={60} sx={{ mt: 1, borderRadius: 1 }} />
      </Box>
    </Stack>
  </Box>
)

export const ChatInterfaceSkeleton = () => (
  <Paper sx={{ height: '100%', p: 2 }}>
    <Stack spacing={2}>
      <ChatMessageSkeleton />
      <ChatMessageSkeleton />
      <ChatMessageSkeleton />
    </Stack>
  </Paper>
)

export const ProgressTrackerSkeleton = () => (
  <Paper sx={{ p: 3 }}>
    <Skeleton variant="text" width="60%" height={32} sx={{ mb: 2 }} />
    <Skeleton variant="rectangular" width="100%" height={8} sx={{ mb: 3, borderRadius: 1 }} />
    <Stack spacing={2}>
      {[1, 2, 3, 4, 5].map((i) => (
        <Box key={i} sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Skeleton variant="circular" width={32} height={32} />
          <Skeleton variant="text" width="40%" height={24} />
        </Box>
      ))}
    </Stack>
  </Paper>
)

export const PageSkeleton = () => (
  <Box>
    <Skeleton variant="text" width="40%" height={48} sx={{ mb: 3 }} />
    <Skeleton variant="rectangular" width="100%" height={400} sx={{ borderRadius: 2 }} />
  </Box>
)

export default {
  ChatMessageSkeleton,
  ChatInterfaceSkeleton,
  ProgressTrackerSkeleton,
  PageSkeleton,
}
