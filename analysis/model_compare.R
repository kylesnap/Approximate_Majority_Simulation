library(tidyverse)
library(feather)

####GETTING RAW FILES AND SAVING THEM AS FEATHERS####

# am.raw <- read_csv('../output/AM_SIMULATIONS_11032020.csv') %>% mutate('MODEL' = 'am')
# bam.raw <- read_csv('../output/BAM_SIMULATIONS_11032020.csv') %>% mutate('MODEL' = 'bam')
# ac.raw <- read_csv('../output/AC_SIMULATIONS_11032020.csv') %>% mutate('MODEL' = 'ac')
# 
am.bots <- read_csv('../output/AM_SIMULATIONS_26032020.csv') %>% mutate('MODEL' = 'am')
bam.bots <- read_csv('../output/BAM_SIMULATIONS_26032020.csv') %>% mutate('MODEL' = 'bam')
# 
# all.raw <- bind_rows(am.raw, bam.raw, ac.raw) 
# write_feather(all.raw, '../output/ALL_SIMULATIONS_11032020.feather')
# 
# ####FEATHER DONE####
# 
# all.raw <- read_feather('../output/ALL_SIMULATIONS_11032020.feather') %>%
#   mutate(SS = NS, BOT_P = 0) %>% bind_rows(., am.bots, bam.bots)
# write_feather(all.raw, '../output/BOT_SIMULATIONS_11032020.feather')

###READ FEATHER
all.raw <- read_feather('../output/BOT_SIMULATIONS_11032020.feather')

####GET MAX####
max_cycle <- all.raw %>%
  filter(CYCLE == 10000, BOT_P == 0) %>%
  group_by(MODEL, NS) %>%
  summarise(MEANY = mean(NY),
            SDY = sd(NY)) %>%
  mutate(LOWERY = lower_ci(MEANY, SDY), UPPERY = upper_ci(MEANY, SDY))

max.plot <- ggplot(max_cycle,
                   aes(NS, MEANY, colour = MODEL, ymin = LOWERY, ymax = UPPERY))
max.plot +
  geom_point() +
  geom_hline(yintercept = 250) +
  geom_errorbar() +
  scale_x_continuous(name = 'Number of Stubborn Bots in Network') +
  scale_y_continuous((name = 'Mean number of y-agents at end of 10,000 cycles')) +
  scale_color_discrete(name = 'Interaction\nModel Used')

####PLOT LEARNING BOTS####
bot_cycle <- all.raw %>%
  filter(CYCLE == 10000, SS <= 150, MODEL != 'ac') %>%
  group_by(MODEL, SS, BOT_P) %>%
  summarise(MEANY = mean(NY),
            SDY = sd(NY)) %>%
  mutate(LOWERY = lower_ci(MEANY, SDY), UPPERY = upper_ci(MEANY, SDY),
         BOT_P = as_factor(BOT_P))

bam_plot <- ggplot(subset(bot_cycle, MODEL == 'bam'), aes(SS, MEANY, colour = BOT_P,
                                                          ymin = LOWERY, max = UPPERY))
bam_plot +
  geom_point() +
  geom_hline(yintercept = 250) +
  geom_errorbar() +
  scale_x_continuous(name = 'Number of Stubborn Bots in Network (BAM)') +
  scale_y_continuous((name = 'Mean number of y-agents at end of 10,000 cycles')) +
  scale_color_discrete(name = 'Prob. of\nBot Learning')

am_plot <- ggplot(subset(bot_cycle, MODEL == 'am'), aes(SS, MEANY, colour = BOT_P,
                                                        ymin = LOWERY, max = UPPERY))
am_plot +
  geom_point() +
  geom_hline(yintercept = 250) +
  geom_errorbar() +
  scale_x_continuous(name = 'Number of Stubborn Bots in Network (AM)') +
  scale_y_continuous((name = 'Mean number of y-agents at end of 10,000 cycles')) +
  scale_color_discrete(name = 'Prob. of\nBot Learning')

####FUNCTION####
upper_ci <- function(MEAN, SD) {
  MEAN + (qt(0.01, 19) * (SD / sqrt(20)))
}

lower_ci <- function(MEAN, SD) {
  MEAN - (qt(0.01, 19) * (SD / sqrt(20)))
}
