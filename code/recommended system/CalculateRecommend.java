package UserIF;
/*
 * 实现UserIF算法
 * 
 * */
public class CalculateRecommend {
	final static int userSum=6040;
	final static int itemSum=3952;
	static double[][]matrixOut;
	static double[][]ItemPref;
	static int[][] recomMatrix;
	//选出与用户u兴趣最接近的K个用户
	public  boolean userSimSort(double[][]simMatrix,int K){
		double[][]matrixIn =new double[userSum+1][userSum+1];
		matrixIn=simMatrix;
		matrixOut =new double[userSum+1][K+1];
		int arrayIndex;//记录要和用户u兴趣最接近的用户ID
		double max;
		for(int u=1;u<=userSum;++u){
			for(int j=K-1;j>=0;--j){
				arrayIndex=0;
				max=matrixIn[u][1];
				for(int v=1;v<=userSum;++v){
					if(max<matrixIn[u][v]){
						max=matrixIn[u][v];
						if(v==userSum)break;
						arrayIndex=v;
					}
					
				}
				matrixOut[u][K-j]=max+arrayIndex;
				matrixIn[u][arrayIndex]=0;
				//此时与用户u最相似的用户v已经被选择了，那么
				//就让他们相似度为0，防止干扰用户u与下一个用户比较
			}
		}
		return true;
	}
	public  boolean recommend(int[][]train,double[][]simMatrix,int K){
		//求用户u对物品i的兴趣度ItemPref[u][i]
		ItemPref =new double[userSum+1][itemSum+1];
		int ID;
		double Wuv=0;		
		for(int u=1;u<=userSum;++u){
			for(int i=1;i<=itemSum;++i){
				if(train[u][i]==0){//向用户u推荐没有过行为的物品i
					for(int v=1;v<=K;++v){
						ID=(int)matrixOut[u][v];
						if(ID==6041){System.out.println("越界"+matrixOut[u][v]);System.exit(0);}
						if(train[ID][i]==1){//用户u没有过行为物品i，但是用户v有行为
							Wuv=matrixOut[u][v]-(double)ID;
							ItemPref[u][i]+=Wuv;
							//System.out.println(ItemPref[u][i]);
							//经过测试，每个结果在0.124左右或者0.247左右波动
							//之所以出现好几个重复的结果是因为用户v有好几个物品是用户u没有的
						}
					}
				}else{
					ItemPref[u][i]=0;
				}
			}
		}
		return true;
	}	

	public boolean getRecommend(int N){//获取针对用户u的推荐列表
		int ID;//物品id号
		double recomDegree;//某个物品对用户u的推荐度
		recomMatrix=new int[userSum+1][N+1];
		for(int u=1;u<=userSum;++u){
			for(int k=1;k<=N;++k){
				recomDegree=ItemPref[u][0];
				ID=0;
				for(int i=1;i<=itemSum;++i){//选择排序，每次选出最大的推荐度的物品i
					if(recomDegree<ItemPref[u][i]){
						recomDegree=ItemPref[u][i];
						ID=i;
					}
				}
				ItemPref[u][ID]=0;//已经比较过的物品i置0，防止下轮的循环又是该物品
				recomMatrix[u][k]=ID;//将第k个推荐的物品存入到推荐矩阵中
			}
		}
		return true;
	}
	
	/*
	 * 测试代码
 	public static void main(String[] args){
			SplitDataToTestAndTrain S=new SplitDataToTestAndTrain();
			Similarity W=new Similarity();
			List<String> data=new ArrayList<String>();
			data=GetDataOfMovieLens.getData();//读到原始数据集
			S.splitData(data,8,3,10);//分解为测试集与训练集
			W.UserSimilarity(S.train);//计算用户相似度，并且保存到simMatrix相似度矩阵中
			userSimSort(Similarity.simMatrix,3);
			recommend(S.train,Similarity.simMatrix,3);//计算用户i对其他用户v推荐给他的物品i的兴趣度
			
		}
		
		*/
}


