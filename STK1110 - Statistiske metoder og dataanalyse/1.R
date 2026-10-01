x <- scan("forsikringskrav.txt")

M1 <- mean(x)
M2 <- mean(x^2)

alpha <- M1^2 / (M2 - M1^2)
gamma <- M1 / (M2 - M1^2)


l <- function(x, alpha, gamma) {
    n <- length(x)
    n * alpha * log(gamma) - n * lgamma(alpha) + 
    (alpha - 1) * sum(log(x)) - gamma * sum(x)
}

negloglikgamma <- function(logalpha,x=x) {
    n <- length(x)
    alpha <- exp(logalpha)
    gamma <- alpha/mean(x)
    logL <- n*alpha*log(gamma)-n*lgamma(alpha)+
    (alpha-1)*sum(log(x))-gamma*sum(x)
    -logL
}


B <- 1000 # Antall bootstrap-simuleringer
n <- length(x)

alpha_boot <- numeric(B)
gamma_boot <- numeric(B)

for (i in 1:B) {
    x_b <- sample(x, size = n, replace = TRUE)
    
    fit_b <- optim(log(alpha), negloglikgamma, x = x_b, method = "BFGS")
    
    alpha_boot[i] <- exp(fit_b$par)
    gamma_boot[i] <- alpha_boot[i] / mean(x_b)
}

# Standardfeil 
se_alpha <- sd(alpha_boot)
se_gamma <- sd(gamma_boot)

# 95% konfidensintervaller
ci_alpha <- quantile(alpha_boot, c(0.025, 0.975))
ci_gamma <- quantile(gamma_boot, c(0.025, 0.975))


mu_boot <- alpha_boot / gamma_boot

ci_mu_95 <- quantile(mu_boot, c(0.025, 0.975))
ci_mu_99 <- quantile(mu_boot, c(0.005, 0.995))

cat("95% CI for mu:\n")
print(ci_mu_95)

cat("\n99% CI for mu:\n")
print(ci_mu_99)