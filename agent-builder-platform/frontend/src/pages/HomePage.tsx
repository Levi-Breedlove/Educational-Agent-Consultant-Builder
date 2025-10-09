import { useNavigate } from 'react-router-dom'
import { Box, Typography, Button, Paper, Grid, Card, CardContent, Container, useTheme } from '@mui/material'
import { AutoAwesome, Speed, Security, AttachMoney } from '@mui/icons-material'

export default function HomePage() {
  const navigate = useNavigate()
  const theme = useTheme()
  const isDark = theme.palette.mode === 'dark'

  const features = [
    {
      icon: <Speed sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: '30-45 Minutes',
      description: 'From idea to production-ready agent',
    },
    {
      icon: <Security sx={{ fontSize: 40, color: isDark ? '#68d391' : 'success.main' }} />,
      title: 'Built with Confidence',
      description: 'Expert AI consultants with validated recommendations',
    },
    {
      icon: <AttachMoney sx={{ fontSize: 40, color: 'warning.main' }} />,
      title: 'Well-Architected',
      description: 'Built on AWS best practices with cost optimization',
    },
  ]

  return (
    <Box
      sx={{
        width: '100%',
        height: '100vh',
        overflow: 'auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Box
        sx={{
          transform: { 
            xs: 'scale(0.45)', 
            sm: 'scale(1)' 
          },
          transformOrigin: 'center center',
          width: { xs: '222%', sm: '100%' },
        }}
      >
      <Container 
        maxWidth="lg" 
        sx={{ 
          py: 6,
          px: 3,
          width: '100%',
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '75vh',
            textAlign: 'center',
            width: '100%',
          }}
        >
        <Paper
          elevation={3}
          sx={{
            p: { xs: 1.25, sm: 3, md: 5 },
            pb: { xs: 1.5, sm: 3, md: 5 },
            borderRadius: { xs: 2, sm: 3 },
            width: '100%',
            maxWidth: { xs: '100%', sm: '100%', md: '1100px' },
            my: { xs: 1, sm: 0 },
            ...(isDark && {
              background: 'rgba(15, 23, 42, 0.4)',
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(104, 211, 145, 0.4)',
              boxShadow: '0 8px 32px rgba(104, 211, 145, 0.2)',
            }),
          }}
        >
          <Box>
            <AutoAwesome
              sx={{
                fontSize: { xs: 36, sm: 60, md: 80 },
                color: isDark ? '#68d391' : 'primary.main',
                mb: { xs: 0.5, sm: 2 },
                filter: isDark ? 'drop-shadow(0 0 20px rgba(104, 211, 145, 0.6))' : 'none',
              }}
            />
            <Typography
              variant="h2"
              gutterBottom
              sx={{
                fontSize: { xs: '1.25rem', sm: '2rem', md: '3rem' },
                mb: { xs: 0.5, sm: 1, md: 1 },
                ...(isDark && {
                  background: 'linear-gradient(135deg, #68d391 0%, #ec4899 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  backgroundClip: 'text',
                }),
              }}
            >
              Agent Builder Platform
            </Typography>
          <Typography
            variant="h5"
            color="text.secondary"
            paragraph
            sx={{
              fontSize: { xs: '0.75rem', sm: '1.15rem', md: '1.35rem' },
              px: { xs: 0.5, sm: 0 },
              mb: { xs: 0.5, sm: 1, md: 1 },
            }}
          >
            Build production-ready AI agents in 30-45 minutes
          </Typography>
          <Typography
            variant="body1"
            color="text.secondary"
            paragraph
            sx={{
              mb: { xs: 1, sm: 3 },
              fontSize: { xs: '0.65rem', sm: '0.95rem' },
              px: { xs: 0.5, sm: 0 },
              lineHeight: { xs: 1.3, sm: 1.6 },
            }}
          >
            Expert AI consultants guide you through requirements, architecture, implementation,
            and deployment with confidence and precision.
          </Typography>

            <Grid container spacing={{ xs: 0.75, sm: 2.5 }} sx={{ mb: { xs: 0.75, sm: 3 }, mt: { xs: 0.25, sm: 1.5 } }}>
              {features.map((feature, index) => (
                <Grid item xs={12} sm={4} key={index}>
                  <Card
                    elevation={0}
                    sx={{
                      height: '100%',
                      position: 'relative',
                      overflow: 'hidden',
                      transition: 'all 0.3s ease',
                      ...(isDark ? {
                        // Dark theme - Hyper-realistic glass with green glow
                        background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.6), rgba(15, 23, 42, 0.4))',
                        backdropFilter: 'blur(12px) saturate(150%)',
                        border: '1px solid rgba(104, 211, 145, 0.4)',
                        borderRadius: 3,
                        boxShadow: `
                          0 8px 32px rgba(104, 211, 145, 0.15),
                          inset 0 1px 0 rgba(255, 255, 255, 0.05),
                          inset 0 -1px 0 rgba(0, 0, 0, 0.2)
                        `,
                        '&::before': {
                          content: '""',
                          position: 'absolute',
                          top: 0,
                          left: 0,
                          right: 0,
                          height: '50%',
                          background: 'linear-gradient(180deg, rgba(255, 255, 255, 0.03), transparent)',
                          pointerEvents: 'none',
                        },
                        '&::after': {
                          content: '""',
                          position: 'absolute',
                          top: '0',
                          left: '0',
                          width: '100%',
                          height: '100%',
                          background: 'radial-gradient(circle at center, rgba(104, 211, 145, 0.05) 0%, transparent 50%)',
                          pointerEvents: 'none',
                        },
                        '&:hover': {
                          border: '1px solid rgba(104, 211, 145, 0.7)',
                          boxShadow: `
                            0 12px 40px rgba(104, 211, 145, 0.3),
                            inset 0 1px 0 rgba(255, 255, 255, 0.15),
                            inset 0 -1px 0 rgba(0, 0, 0, 0.2)
                          `,
                        },
                      } : {
                        // Light theme - Clean glass with green border
                        background: 'linear-gradient(135deg, rgba(248, 250, 252, 0.7), rgba(241, 245, 249, 0.6))',
                        backdropFilter: 'blur(10px)',
                        border: '1px solid rgba(104, 211, 145, 0.4)',
                        borderRadius: 3,
                        boxShadow: `
                          0 4px 16px rgba(72, 187, 120, 0.1),
                          inset 0 1px 0 rgba(255, 255, 255, 0.5)
                        `,
                        '&::before': {
                          content: '""',
                          position: 'absolute',
                          top: 0,
                          left: 0,
                          right: 0,
                          height: '50%',
                          background: 'linear-gradient(180deg, rgba(255, 255, 255, 0.3), transparent)',
                          pointerEvents: 'none',
                        },
                        '&:hover': {
                          border: '1px solid rgba(104, 211, 145, 0.7)',
                          boxShadow: `
                            0 8px 24px rgba(72, 187, 120, 0.25),
                            inset 0 1px 0 rgba(255, 255, 255, 0.9)
                          `,
                        },
                      }),
                    }}
                  >
                    <CardContent
                      sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        textAlign: 'center',
                        px: { xs: 1, sm: 2 },
                        pt: { xs: 1.5, sm: 3 },
                        pb: { xs: 1.5, sm: 3 },
                        minHeight: { xs: 110, sm: 160 },
                      }}
                    >
                      <Box sx={{ mt: 0 }}>
                        <Box sx={{ fontSize: { xs: 32, sm: 40 }, display: 'flex', justifyContent: 'center' }}>
                          {feature.icon}
                        </Box>
                      </Box>
                      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                        <Typography 
                          variant="h6" 
                          gutterBottom 
                          sx={{ 
                            mb: { xs: 0.25, sm: 1 }, 
                            mt: { xs: 0.5, sm: 1.5 },
                            fontSize: { xs: '0.75rem', sm: '1rem' },
                            lineHeight: 1.2,
                          }}
                        >
                          {feature.title}
                        </Typography>
                        <Typography 
                          variant="body2" 
                          color="text.secondary"
                          sx={{
                            fontSize: { xs: '0.6rem', sm: '0.75rem' },
                            lineHeight: { xs: 1.2, sm: 1.3 },
                            width: '100%',
                            whiteSpace: { xs: 'normal', sm: 'nowrap' },
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                          }}
                        >
                          {feature.description}
                        </Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Box
              sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                width: '100%',
                mt: { xs: 0.75, sm: 4 },
                px: { xs: 0.5, sm: 0 },
              }}
            >
              <Box
                sx={{
                  position: 'relative',
                  display: 'inline-block',
                  width: { xs: '100%', sm: 'auto' },
                }}
              >
              {/* Animated LED border with glow - translucent but colorful */}
              <Box
                sx={{
                  position: 'absolute',
                  inset: '-3px',
                  borderRadius: '30px',
                  background: 'linear-gradient(90deg, #d946ef, #ff1493, #ffd700, #00ff7f, #00bfff, #ba55d3, #d946ef)',
                  backgroundSize: '200% 100%',
                  animation: 'ledFlow 3s linear infinite',
                  opacity: isDark ? 0.7 : 0,
                  filter: 'blur(4px)',
                  '@keyframes ledFlow': {
                    '0%': {
                      backgroundPosition: '0% 50%',
                    },
                    '100%': {
                      backgroundPosition: '200% 50%',
                    },
                  },
                }}
              />
              
              {/* Glass-like textured border */}
              <Box
                sx={{
                  position: 'absolute',
                  inset: '0',
                  borderRadius: '30px',
                  border: '3px solid transparent',
                  backgroundImage: 'linear-gradient(135deg, rgba(255, 255, 255, 0.4), rgba(128, 128, 128, 0.2), rgba(255, 255, 255, 0.3))',
                  backgroundOrigin: 'border-box',
                  backgroundClip: 'border-box',
                  WebkitMask: 'linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0)',
                  WebkitMaskComposite: 'xor',
                  maskComposite: 'exclude',
                  opacity: isDark ? 1 : 0,
                  pointerEvents: 'none',
                  zIndex: 2,
                }}
              />
              
              {/* Crystalline glass edge */}
              <Box
                sx={{
                  position: 'absolute',
                  inset: '-1px',
                  borderRadius: '30px',
                  background: 'linear-gradient(135deg, rgba(255,255,255,0.3), rgba(255,255,255,0.05))',
                  opacity: isDark ? 0.3 : 0,
                  pointerEvents: 'none',
                }}
              />
              
              <Button
                variant="contained"
                size="medium"
                startIcon={<AutoAwesome sx={{ color: '#68d391', fontSize: { xs: 18, sm: 24 } }} />}
                onClick={() => navigate('/builder')}
                fullWidth
                sx={{
                  position: 'relative',
                  zIndex: 3,
                  px: { xs: 2, sm: 3.5 },
                  py: { xs: 0.75, sm: 1 },
                  fontSize: { xs: '0.75rem', sm: '0.95rem' },
                  fontWeight: 600,
                  borderRadius: '30px',
                  maxWidth: { xs: '100%', sm: 'none' },
                  ...(isDark ? {
                    background: 'linear-gradient(135deg, rgb(15, 23, 42), rgb(10, 18, 35))',
                    border: '1px solid rgba(104, 211, 145, 0.5)',
                    boxShadow: '0 4px 15px rgba(104, 211, 145, 0.3), inset 0 1px 0 rgba(255,255,255,0.1)',
                    '&:hover': {
                      background: 'linear-gradient(135deg, rgb(20, 28, 50), rgb(15, 23, 42))',
                      border: '1px solid rgba(104, 211, 145, 0.7)',
                      boxShadow: '0 6px 20px rgba(104, 211, 145, 0.4), inset 0 1px 0 rgba(255,255,255,0.15)',
                    },
                    '&:active': {
                      transform: 'translateY(2px) scale(0.98)',
                      boxShadow: '0 0 40px rgba(104, 211, 145, 0.6), 0 0 60px rgba(104, 211, 145, 0.5), inset 0 1px 0 rgba(255,255,255,0.2)',
                    },
                  } : {
                    background: 'linear-gradient(135deg, #68d391 0%, #48bb78 100%)',
                    color: '#000',
                    '&:active': {
                      transform: 'translateY(2px) scale(0.98)',
                    },
                  }),
                  transition: 'all 0.2s ease',
                }}
              >
                <Box
                  component="span"
                  sx={{
                    ...(isDark && {
                      background: 'linear-gradient(135deg, #68d391 0%, #ec4899 100%)',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                      backgroundClip: 'text',
                    }),
                  }}
                >
                  Start Building
                </Box>
              </Button>
              </Box>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
      </Box>
    </Box>
  )
}
