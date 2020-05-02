library(tidyverse)
library(feather)

####GETTING RAW FILES AND SAVING THEM AS FEATHERS####

#am.raw <- read_csv('../output/AM_SIMULATIONS_20042020.csv') %>% bind_rows(., read_csv('../output/AM_SIMULATIONS_11042020.csv')) %>% 
#  mutate('MODEL' = 'am') %>% distinct()
#bam.raw <- read_csv('../output/BAM_SIMULATIONS_20042020.csv') %>% bind_rows(., read_csv('../output/BAM_SIMULATIONS_12042020.csv')) %>% 
#  mutate('MODEL' = 'bam') %>% distinct()
#ac.raw <- read_csv('../output/ac_simulations_12042020.csv') %>% mutate('model' = 'ac') %>%
#  distinct()
 
#all.raw <- bind_rows(am.raw, bam.raw, ac.raw)
#w#rite_feather(all.raw, '../output/ALL_SIMULATIONS_NEWINT.feather')
## 
# ####FEATHER DONE####
# 

###READ FEATHER
all.raw <- read_feather('../output/ALL_SIMULATIONS_NEWINT.feather')

####GET MAX####
max_cycle <- all.raw %>%
  group_by(MODEL, NS, TRIAL) %>%
  filter(CYCLE == max(CYCLE), BOT_P == 0) %>%
  ungroup() %>%
  group_by(MODEL, NS) %>%
  summarise(MEANY = mean(NY),
            SDY = sd(NY)) %>%
  mutate(LOWERY = lower_ci(MEANY, SDY), UPPERY = upper_ci(MEANY, SDY)) %>%
  mutate_at(vars(contains('Y')), to_prop)

max.plot <- ggplot(max_cycle,
                   aes(NS, MEANY, colour = MODEL, ymin = LOWERY, ymax = UPPERY))
max.plot +
  geom_point() +
  geom_hline(yintercept = 0.5, linetype = 'dashed') +
  geom_linerange() +
  geom_line() +
  scale_x_continuous(name = 'Number of Stubborn Bots in Network', breaks = c(seq(0, 250, 50))) +
  scale_y_continuous(name = 'Mean y-prop at Simulation Termination') +
  scale_color_discrete(name = 'Interaction\nModel Used') +
  theme_classic() + 
  theme(text = element_text(size = 12, family ='serif'))
  

####PLOT MIN. CYCLES REQUIRED TO CROSS 0.5####
min_cycle <- all.raw %>%
  group_by(MODEL, NS, TRIAL) %>%
  filter(NY >= 250, BOT_P == 0, NS >= 80, MODEL != 'AC') %>%
  filter(CYCLE == min(CYCLE)) %>%
  ungroup() %>%
  group_by(MODEL, NS) %>%
  summarise(MEANC = mean(CYCLE),
            SDC = sd(CYCLE)) %>%
  mutate(LOWERC = lower_ci(MEANC, SDC), UPPERC = upper_ci(MEANC, SDC),
         NORMC = 1 / (MEANC))


model.blocked <- lm(NORMC ~ NS * MODEL, data = min_cycle)
anova(model.blocked)

min.plot <- ggplot(min_cycle,
                   aes(NS, MEANC, fill = MODEL, ymin = LOWERC, ymax = UPPERC))

min.plot +
  geom_bar(stat = 'identity', position = 'dodge', size = 0.5) +
  geom_linerange(position = position_dodge(10)) +
  scale_x_continuous(name = 'Number of Stubborn Bots in Network') +
  scale_y_continuous(name = 'Mean Number of Cycles Before Network Majority Switch') +
  scale_fill_discrete(name = 'Interaction\nModel Used') +
  theme_classic() + 
  theme(text = element_text(size = 12, family ='serif'))


####FUNCTION####
upper_ci <- function(MEAN, SD) {
  MEAN + (qt(.95/2 + 0.5, 19) * (SD / sqrt(20)))
}

lower_ci <- function(MEAN, SD) {
  MEAN - (qt(.95/2 + 0.5, 19) * (SD / sqrt(20)))
}

to_prop <- function(x) { x / 500 }
