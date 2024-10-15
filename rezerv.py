##class CostUpdateFrontView(LoginRequiredMixin,APIView):
##
##    renderer_classes = [TemplateHTMLRenderer]
##    template_name = 'costs/cost_update.html'
##    
##    def get(self, request,pk):
##        cost=Cost.objects.get(id=pk)
##        serializer=CostSerializer(cost)
##        return Response({'serializer':serializer,'category':cost})       
##    def post(self,request,pk):     
##        cost=Cost.objects.get(id=pk)
##        serializer=CostCreateSerializer(cost,data=request.data)
##        if serializer.is_valid():
##            serializer.save()
##            return redirect('costs_front_list_url')
##        else:
##            return Response({'serializer':serializer,'category':cost})   ##class CostCreateFrontView(ObjectCreateMixin, LoginRequiredMixin,APIView):
##
##    renderer_classes = [TemplateHTMLRenderer]
##    template_name = 'costs/cost_create.html'
##
##    def get(self,request):
##        serializer=CostCreateSerializer()#initial={'cost_date':date.today()})
##        return Response({'serializer':serializer})
##        
##    
##    def post(self,request):
##
##        serializer=CostCreateSerializer(data=request.data)
##        if serializer.is_valid():            
##            serializer.save()
##            return redirect('costs_front_list_url')
##        else:
##            return Response({'serializer':serializer})
##class DayCostDetailView(LoginRequiredMixin,View):
##
##    def get(self,request, year, month, day):
##        if DayCost.objects.filter(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day).exists():
##            day_cost=DayCost.objects.get(user=request.user.username,day_date__year=year,day_date__month=month,day_date__day=day)
##            return render(request,'costs/day_cost_detail.html',{'day_cost':day_cost,'user':request.user})
##                                                                
##        else:
##            return render(request,'costs/day_cost_detail.html',{'date':date(year, month, day),'user':request.user,'message':'расходов не было'})
##
##    
##    def get(self, request,pk):
##        category=CategoryCost.objects.get(id=pk)
##        serializer=CategoryCostSerializer(category)
##        return Response({'serializer':serializer,'category':category})       
##    def post(self,request,pk):     
##        category=CategoryCost.objects.get(id=pk)
##        serializer=CategoryCostCreateSerializer(category,data=request.data)
##        if serializer.is_valid():
##            serializer.save()
##            return redirect('category_cost_front_list_url')
##        else:
##            return Response({'serializer':serializer,'category':category})   
##
##    
##    def get(self, request,pk):
##        cost=Cost.objects.get(id=pk)
##        serializer=CostSerializer(cost)
##        return Response({'serializer':serializer,'category':cost})       
##    def post(self,request,pk):     
##        cost=Cost.objects.get(id=pk)
##        serializer=CostCreateSerializer(cost,data=request.data)
##        if serializer.is_valid():
##            serializer.save()
##            return redirect('costs_front_list_url')
##        else:
##            return Response({'serializer':serializer,'category':cost})   
##    def get(self, request, pk):
##        category=CategoryCost.objects.get(id=pk)
##        return render(request, 'costs/category_cost_delete.html', context={'category':category})
##
##     
##    def post(self,request,pk):     
##        category=CategoryCost.objects.get(id=pk)
##        category.delete()
##        return redirect(reverse('category_cost_front_list_url'))
##
##     def get(self, request, pk):
##        cost=Cost.objects.get(id=pk)
##        return render(request, 'costs/cost_delete.html', context={'cost':cost})
##
##     
##     def post(self,request,pk):     
##        cost=Cost.objects.get(id=pk)
##        cost.delete()
##        return redirect(reverse('costs_front_list_url'))
##    def get(self, request):
##        categories=CategoryCost.objects.all()
##        serializer=CategoryCostSerializer(categories,many=True)
##        return Response({'categories':categories})

##class CategoryCostDetailFrontView( LoginRequiredMixin,APIView):
##
##    serializer=None
##    template_name = None
##    model=None
##
##    renderer_classes = [TemplateHTMLRenderer]
##    template_name = 'costs/category_cost_detail.html'
##
##    def get(self, request,pk):
##        category=CategoryCost.objects.get(id=pk)
##        serializer=CategoryCostSerializer(category)
##        return Response({'category':category})


##    def get(self, request,pk):
##        cost=Cost.objects.get(id=pk)
##        serializer=CostSerializer(cost)
##        return Response({'cost':cost})
