B <- 10000
n <- 15
mu_sann <- 558
sigma_sann <- 30

sim_data <- matrix(
    rnorm(B * n, mean = mu_sann, sd = sigma_sann), 
    nrow = B, 
    ncol = n
)

# b
x_bar <- rowMeans(sim_data)
s <- apply(sim_data, 1, sd)
t_val <- qt(0.975, df = n - 1)
feilmargin <- t_val * s / sqrt(n)

nedre_grense <- x_bar - feilmargin
ovre_grense <- x_bar + feilmargin

dekker_mu <- (nedre_grense <= mu_sann) & (ovre_grense >= mu_sann)

andel <- mean(dekker_mu)

#c
feilmargin_stor <- 1.96 * s / sqrt(n)

nedre_grense_stor <- x_bar - feilmargin_stor
ovre_grense_stor <- x_bar + feilmargin_stor

dekker_mu_stor <- (nedre_grense_stor <= mu_sann) & (ovre_grense_stor >= mu_sann)

andel_stor <- mean(dekker_mu_stor)

#d
chi_nedre <- qchisq(0.025, df = n - 1)
chi_ovre  <- qchisq(0.975, df = n - 1)

nedre_grense_sigma <- sqrt((n - 1) * s^2 / chi_ovre)
ovre_grense_sigma  <- sqrt((n - 1) * s^2 / chi_nedre)

dekker_sigma <- (nedre_grense_sigma <= sigma_sann) & 
                (ovre_grense_sigma >= sigma_sann)
andel_sigma <- mean(dekker_sigma)

cat("Andel intervaller som inneholder 30:", andel_sigma, "\n")
