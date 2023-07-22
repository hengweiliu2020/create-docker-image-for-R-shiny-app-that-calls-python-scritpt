library(reticulate)
library(shiny)

ui <- fluidPage(
  tableOutput(outputId = "table01")
)

server <- function(input, output, session){
  
  reticulate::source_python('summary.py')
 
  
  output$table01 <- renderTable({
  print(outdata)
    
  })
  
}

shinyApp(ui, server)
