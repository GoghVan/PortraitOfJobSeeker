package UserIF;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

public class Start {
	final static int userSum=6040;
	final static int itemSum=3952;
	public static void main(String[] args){
		double start=System.currentTimeMillis();
		int N=10;//向用户推荐的物品个数
		int K=160;//和某一用户兴趣最接近的K个用户
		double coverage,popularity;
		double[]rp=new double[2];
		SplitDataToTestAndTrain S=new SplitDataToTestAndTrain();
		Similarity W=new Similarity();
		CalculateRecommend CR=new CalculateRecommend();
		EvaluationIndices EI=new EvaluationIndices();
		List<String> data=new ArrayList<String>();
		data=GetDataOfMovieLens.getData();//读到原始数据集
		S.splitData(data,8,3,10);//分解为测试集与训练集
		W.UserSimilarity(S.train);//计算用户相似度，并且保存到simMatrix相似度矩阵中
		CR.userSimSort(Similarity.simMatrix,K);
		CR.recommend(S.train,Similarity.simMatrix,K);//计算用户i对其他K个用户推荐给他的物品i的兴趣度
		CR.getRecommend(N);//获取对每个用户的推荐列表
		rp=EI.recallAndPrecision(S.train,S.test, N);
		coverage=EI.coverage(S.train,N);
		popularity=EI.popularity(S.train, N);
		DecimalFormat df1 = new DecimalFormat("0.00%");
		DecimalFormat df2 = new DecimalFormat("0.000001");
		System.out.println("K为"+K+"时");
		System.out.print("准确率"+df1.format(rp[0]));
		System.out.print("召回率"+df1.format(rp[1]));
		System.out.print("覆盖率"+df1.format(coverage));
		System.out.print("流行度"+df2.format(popularity));
		double end=System.currentTimeMillis();
		System.out.println("程序运行的时间为："+(end-start)/1000+"秒");
	}
}
