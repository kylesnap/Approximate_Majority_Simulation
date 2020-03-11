library(tidyverse)
library(feather)

####GETTING RAW FILES AND SAVING THEM AS FEATHERS####

am.raw <- read_csv('../output/AM_SIMULATIONS_11032020.csv') %>% mutate('MODEL' = 'am')
bam.raw <- read_csv('../output/BAM_SIMULATIONS_11032020.csv') %>% mutate('MODEL' = 'bam')
ac.raw <- read_csv('../output/AC_SIMULATIONS_11032020.csv') %>% mutate('MODEL' = 'ac')

all.raw <- bind_rows(am.raw, bam.raw, ac.raw)
write_feather(all.raw, '../output/ALL_SIMULATIONS_11032020.feather')

####FEATHER DONE####

all.raw <- read_feather('../output/ALL_SIMULATIONS_11032020.feather')

####GET MAX####
max_cycle <- all.raw %>% filter(CYCLE == 10000) %>%
  group_by(MODEL, NS) %>%
  summarise(MEANY = mean(NY),
            SDY = sd(NY)) %>%
  mutate(LOWERY = lower_ci(MEANY, SDY), UPPERY = upper_ci(MEANY, SDY))

max.plot <- ggplot(max_cycle, 
                   aes(NS, MEANY, colour = MODEL, ymin = LOWERY, ymax = UPPERY))
max.plot + geom_point() +
  geom_hline(yintercept = 250) + geom_errorbar()




####FUNCTION####
upper_ci <- function(MEAN, SD) {
  MEAN + ( qt(0.01, 19) * (SD / sqrt(20)) )
}

lower_ci <- function(MEAN, SD) {
  MEAN - ( qt(0.01, 19) * (SD / sqrt(20)) )
}
