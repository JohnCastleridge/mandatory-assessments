B <- 10000
n <- 15
mu_sann <- 558
sigma_sann <- 30

#e
sim_data <- mu_sann + sigma_sann * matrix(
    rt(B * n, df=7), 
    nrow = B, 
    ncol = n
)


x_bar <- rowMeans(sim_data)
s <- apply(sim_data, 1, sd)
t_val <- qt(0.975, df = n - 1)
feilmargin <- t_val * s / sqrt(n)

nedre_grense <- x_bar - feilmargin
ovre_grense <- x_bar + feilmargin

dekker_mu <- (nedre_grense <= mu_sann) & (ovre_grense >= mu_sann)

andel <- mean(dekker_mu)

#f
chi_nedre <- qchisq(0.025, df = n - 1)
chi_ovre  <- qchisq(0.975, df = n - 1)

nedre_grense_sigma <- sqrt((n - 1) * s^2 / chi_ovre)
ovre_grense_sigma  <- sqrt((n - 1) * s^2 / chi_nedre)

nedre_grense_sigma <- sqrt((n - 1) * s^2 / chi_ovre)
ovre_grense_sigma  <- sqrt((n - 1) * s^2 / chi_nedre)

sigma_tilde <- sigma_sann * sqrt(7 / (7 - 2))
dekker_sigma_tilde <- (nedre_grense_sigma <= sigma_tilde) & (ovre_grense_sigma >= sigma_tilde)
andel_sigma_tilde <- mean(dekker_sigma_tilde)

cat("Andel intervaller som inneholder sigma_tilde:", andel_sigma_tilde, "\n")