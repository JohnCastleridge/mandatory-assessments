
x <- c(525, 587, 547, 558, 591, 531, 571, 551, 566, 622, 561, 502, 556, 565, 562)
n <- 15

x_bar <- mean(x)
s <- sd(x)
t_val <- qt(0.975, df = n - 1)

nedre <- x_bar - t_val * s / sqrt(n)
ovre <- x_bar + t_val * s / sqrt(n)
