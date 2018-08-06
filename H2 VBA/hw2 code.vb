Sub Worksheet()

For Each ws In Worksheets
    
    Dim row As Long
    row = ws.Cells(Rows.Count, 1).End(xlUp).row
    
    Dim column As Long
    column = ws.Cells(1, Columns.Count).End(xlToLeft).column
    
    ws.Cells(1, 9).Value = "Ticker"
    ws.Cells(1, 10).Value = "Yearly Change"
    ws.Cells(1, 11).Value = "Percent Change"
    ws.Cells(1, 12).Value = "Total Stock Volume"
    ws.Cells(2, 15).Value = "Greatest % Increase"
    ws.Cells(3, 15).Value = "Greatest % Decrease"
    ws.Cells(4, 15).Value = "Greatest Total Volume"
    ws.Cells(1, 16).Value = "Ticker"
    ws.Cells(1, 17).Value = "Value"
    
    Dim i As Long
    Dim ticker As String
    Dim total As Double
    Dim ticker_row As Integer
    Dim open_price As Double
    Dim close_price As Double
    
    ticker = ws.Cells(2, 1).Value
    total = 0
    ticker_row = 2
    open_price = ws.Cells(2, 3).Value
    
    For i = 2 To row
        If ticker = ws.Cells(i, 1).Value Then
            total = total + ws.Cells(i, 7).Value
        Else
            ws.Cells(ticker_row, 9).Value = ticker
            ws.Cells(ticker_row, 12).Value = total
            close_price = ws.Cells(i - 1, 6).Value
            ws.Cells(ticker_row, 10).Value = close_price - open_price
            
            If ws.Cells(ticker_row, 10).Value > 0 Then
                ws.Cells(ticker_row, 10).Interior.Color = vbGreen
            Else
                ws.Cells(ticker_row, 10).Interior.Color = vbRed
            End If
            
            If open_price <> 0 Then
                ws.Cells(ticker_row, 11).Value = Format((close_price - open_price) / open_price, "percent")
            Else
                ws.Cells(ticker_row, 11).Value = Format(0, "percent")
            End If
            
            open_price = ws.Cells(i, 3).Value
            total = 0
            ticker = ws.Cells(i, 1).Value
            ticker_row = ticker_row + 1
        End If
    Next i
    
    ws.Cells(ticker_row, 9).Value = ticker
    ws.Cells(ticker_row, 12).Value = total
    close_price = ws.Cells(row, 6).Value
    ws.Cells(ticker_row, 10).Value = close_price - open_price
            
    If ws.Cells(ticker_row, 10).Value > 0 Then
        ws.Cells(ticker_row, 10).Interior.Color = vbGreen
    Else
        ws.Cells(ticker_row, 10).Interior.Color = vbRed
    End If
    
    If open_price <> 0 Then
        ws.Cells(ticker_row, 11).Value = Format((close_price - open_price) / open_price, "percent")
    Else
        ws.Cells(ticker_row, 11).Value = Format(0, "percent")
    End If
    
    ws.Cells(ticker_row, 11).Value = Format((open_price - close_price) / open_price, "percent")
    
    
    
    Dim max_per As Double
    Dim min_per As Double
    Dim max_vol As Double
    Dim curr_ticker As String
    
    max_per = ws.Cells(2, 11).Value
    min_per = ws.Cells(2, 11).Value
    max_vol = ws.Cells(2, 12).Value
    curr_ticker = ws.Cells(2, 9).Value
    
    ws.Cells(2, 16).Value = curr_ticker
    ws.Cells(3, 16).Value = curr_ticker
    ws.Cells(4, 16).Value = curr_ticker
    ws.Cells(2, 17).Value = max_per
    ws.Cells(3, 17).Value = min_per
    ws.Cells(4, 17).Value = max_vol
    
    For i = 2 To ticker_row
        If ws.Cells(i, 11).Value > max_per Then
            max_per = ws.Cells(i, 11).Value
            curr_ticker = ws.Cells(i, 9).Value
            ws.Cells(2, 16).Value = curr_ticker
            ws.Cells(2, 17).Value = Format(max_per, "percent")
        End If
    Next i
    
    For i = 2 To ticker_row
        If ws.Cells(i, 11).Value < min_per Then
            min_per = ws.Cells(i, 11).Value
            curr_ticker = ws.Cells(i, 9).Value
            ws.Cells(3, 16).Value = curr_ticker
            ws.Cells(3, 17).Value = Format(min_per, "percent")
        End If
    Next i
    
    For i = 2 To ticker_row
        If ws.Cells(i, 12).Value > max_vol Then
            max_vol = ws.Cells(i, 12).Value
            curr_ticker = ws.Cells(i, 9).Value
            ws.Cells(4, 16).Value = curr_ticker
            ws.Cells(4, 17).Value = max_vol
        End If
    Next i
        
    

Next ws

End Sub
