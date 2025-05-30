bubble_sort <- function(vec){
  n <- length(vec)
  for(i in 1:(n-1)){
    counter <- 0
    for(j in 1:(n-i)){
      if(vec[j] > vec[j+1]){
        counter <- counter + 1
        x <- vec[j]
        vec[j] <- vec[j+1]
        vec[j+1] <- x
      }
    }
    if(counter == 0){
      return(vec)
    }
  }
  return(vec)
}


vec <- readline("Enter numbers separated by space: ")
vec <- as.numeric(strsplit(vec, " ")[[1]])
vec <- bubble_sort(vec)

print(vec)